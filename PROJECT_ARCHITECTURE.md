# 🏗️ Quran Coach Project Architecture Guide

## 📁 **Project Structure Overview**

```
Quran-Recitation-Analyst/
├── 📄 TASK.md                     # Project roadmap and progress tracking
├── 📄 ai_powered_quran_coach_setup_guide.md  # Original setup guide
├── 📄 PROJECT_ARCHITECTURE.md     # This file - architecture explanation
├── 📄 setup_instructions.md       # Environment setup guide
└── backend/                       # FastAPI backend application
    ├── 📄 requirements.txt        # Python dependencies
    ├── 📄 env_setup.md           # Environment variables guide
    ├── 📁 quran_coach_env/        # Virtual environment (created after setup)
    └── app/                       # Main application package
        ├── 📄 main.py             # FastAPI application entry point
        ├── 📄 database.py         # Database connection and configuration
        ├── 📁 models/             # Data models (SQLModel/Pydantic)
        │   ├── 📄 __init__.py     # Package exports
        │   ├── 📄 sessions.py     # Session data models
        │   ├── 📄 insights.py     # AI insights models
        │   ├── 📄 mistakes.py     # Mistake tracking models
        │   ├── 📄 portion_details.py  # Quran portion models
        │   ├── 📄 test_types.py   # Testing method models
        │   └── 📄 learning_methods.py  # Learning approach models
        ├── 📁 routers/            # API endpoints (FastAPI routers)
        │   ├── 📄 __init__.py     # Package exports
        │   ├── 📄 auth.py         # Authentication endpoints
        │   ├── 📄 sessions.py     # Session CRUD endpoints
        │   └── 📄 insights.py     # AI insights endpoints
        └── 📁 services/           # Business logic and external services
            ├── 📄 __init__.py     # Package exports
            ├── 📄 ai_service.py   # Base AI service class
            ├── 📄 gemini_service.py   # Gemini AI integration
            └── 📄 whisper_service.py  # OpenAI Whisper integration
```

---

## 🔍 **File-by-File Breakdown**

### **Root Level Files**

#### 📄 `TASK.md`

- **Purpose**: Project roadmap with detailed tasks and timeline
- **Contains**: 3-day development plan, task checkboxes, technical specifications
- **Used by**: Development team to track progress and next steps

#### 📄 `ai_powered_quran_coach_setup_guide.md`

- **Purpose**: Original project specification and design document
- **Contains**: Database schema, API requirements, deployment instructions
- **Used by**: Understanding project requirements and initial planning

---

### **Backend Application Structure**

#### 📄 `backend/requirements.txt`

- **Purpose**: Lists all Python package dependencies
- **Key packages**:
  - `fastapi`: Web framework for building APIs
  - `sqlmodel`: Database ORM (combines SQLAlchemy + Pydantic)
  - `psycopg2-binary`: PostgreSQL database adapter
  - `openai`: OpenAI API client (for Whisper)
  - `google-generativeai`: Gemini AI client
  - `uvicorn`: ASGI server to run FastAPI
  - `pytest`: Testing framework

#### 📄 `backend/app/main.py` - **🚪 Application Entry Point**

```python
# What it does:
1. Creates FastAPI application instance
2. Configures CORS (Cross-Origin Resource Sharing)
3. Includes all API routers
4. Sets up global exception handling
5. Defines startup events (database initialization)
6. Provides health check endpoints

# Key components:
- app = FastAPI() # Main application
- CORS middleware for frontend communication
- Router inclusion: /api/auth, /api/sessions, /api/insights
- Global error handling
- Database startup initialization
```

#### 📄 `backend/app/database.py` - **🗄️ Database Layer**

```python
# What it does:
1. Manages Supabase PostgreSQL connection
2. Creates SQLModel engine with connection pooling
3. Provides database session dependency for FastAPI
4. Handles database table creation
5. Tests database connectivity

# Key components:
- Engine creation with connection string
- get_db() dependency function
- Connection pooling and error handling
- SQLModel table creation
```

---

### **📁 Models Package** - **Data Structure Definitions**

All model files follow the same pattern:

#### 📄 `sessions.py` - **Session Data Models**

```python
# Contains 4 model classes:

1. SessionBase(SQLModel):
   - Common fields shared across all session schemas
   - user_id, timestamp, duration, performance_score, notes

2. Session(SessionBase, table=True):
   - Database table model with relationships
   - __tablename__ = "sessions"
   - Relationships to mistakes, portions, test_types, learning_methods

3. SessionCreate(SessionBase):
   - Schema for creating new sessions via API
   - Validation rules for input data

4. SessionRead(SessionBase):
   - Schema for returning session data from API
   - Includes id, timestamps, and optional related data

5. SessionUpdate(SQLModel):
   - Schema for updating existing sessions
   - All fields optional for partial updates
```

#### 📄 `mistakes.py` - **Mistake Tracking Models**

```python
# Tracks Quran recitation errors:
- MistakeBase: location, error_category, error_subcategory, details
- Mistake: Database model with foreign key to sessions
- Enums: ResolutionStatus (pending, practicing, resolved)
- Validation: severity_level (1-5), resolution tracking
```

#### 📄 `insights.py` - **AI Insights Models**

```python
# Stores AI-generated coaching insights:
- InsightBase: summary, next_actions (JSONB), confidence_score
- Insight: Database model linked to users
- Enums: InsightType (general, weakness_focus, etc.)
- Features: Expiration dates, structured recommendations
```

#### 📄 `portion_details.py` - **Quran Portion Models**

```python
# Tracks which Quran portions were practiced:
- PortionDetailBase: portion_type, reference, recency_category
- Enum: RecencyCategory (new, recent, reviewing, maintenance)
- Examples: "Surah Al-Fatiha", "2:1-10", "Juz 1"
```

#### 📄 `test_types.py` & `learning_methods.py`

```python
# Track testing methods and learning approaches:
- TestType: category, description, success_rate
- LearningMethod: method_type, details, effectiveness_rating
- Examples: "recitation test", "repetition method", "audio learning"
```

---

### **📁 Routers Package** - **API Endpoints**

#### 📄 `routers/auth.py` - **Authentication System**

```python
# Handles user authentication:

Current Implementation (MVP):
- Placeholder authentication for development
- get_current_user() dependency function
- Login/register endpoints (mock for now)
- JWT token structure prepared

Future Integration:
- Will integrate with Supabase Auth
- Real JWT validation
- User session management
```

#### 📄 `routers/sessions.py` - **Session Management API**

```python
# Complete CRUD operations for practice sessions:

Endpoints:
POST   /api/sessions/           # Create new session
GET    /api/sessions/           # List user's sessions
GET    /api/sessions/{id}       # Get specific session
PUT    /api/sessions/{id}       # Update session
DELETE /api/sessions/{id}       # Delete session
POST   /api/sessions/{id}/mistakes     # Add mistake to session
POST   /api/sessions/{id}/portions     # Add portion to session
POST   /api/sessions/{id}/audio        # Upload audio file

Features:
- User isolation (RLS)
- Pagination support
- File upload handling
- Error handling with rollback
```

#### 📄 `routers/insights.py` - **AI Insights API**

```python
# Manages AI-generated coaching insights:

Endpoints:
GET    /api/insights/           # Get user's insights
GET    /api/insights/{id}       # Get specific insight
POST   /api/insights/generate   # Generate new insights
GET    /api/insights/stats/overview  # User statistics
PUT    /api/insights/{id}       # Update insight
DELETE /api/insights/{id}       # Delete insight

Features:
- AI analysis trigger
- Statistics calculation
- Filtering by insight type
- Confidence scoring
```

---

### **📁 Services Package** - **Business Logic & AI**

#### 📄 `services/ai_service.py` - **Base AI Service Class**

```python
# Abstract base class for all AI services:

Features:
- Common error handling
- API key validation
- Retry logic with exponential backoff
- Standardized result format (AIAnalysisResult)
- Input validation
- Rate limiting protection

Design Pattern: Template Method Pattern
- Defines common structure
- Subclasses implement specific AI logic
```

#### 📄 `services/gemini_service.py` - **Gemini AI Integration**

```python
# Google Gemini AI for text analysis:

Capabilities:
1. analyze_mistakes():
   - Analyzes mistake patterns
   - Provides categorization and recommendations
   - Returns structured JSON with focus areas

2. generate_insights():
   - Creates personalized coaching insights
   - Analyzes session data trends
   - Generates review schedules and recommendations

3. categorize_mistake():
   - Single mistake classification
   - Severity assessment
   - Correction method suggestions

Models Used: gemini-1.5-pro
Output Format: JSON with confidence scores
```

#### 📄 `services/whisper_service.py` - **Audio Transcription**

```python
# OpenAI Whisper for audio processing:

Capabilities:
1. transcribe_audio():
   - Converts audio to text
   - Optimized for Arabic/Quranic content
   - Returns text with confidence scores

2. transcribe_with_timestamps():
   - Word-level timestamps
   - Segment analysis
   - Detailed timing information

3. detect_language():
   - Automatic language detection
   - Supports multiple languages

4. validate_audio_file():
   - File size validation (25MB limit)
   - Format checking
   - Error prevention

Features:
- Arabic language optimization
- Quranic vocabulary prompts
- Temporary file handling
- Confidence calculation
```

---

## 🔄 **Data Flow Architecture**

### **1. Session Creation Flow**

```
Frontend → POST /api/sessions/ → sessions.py router →
SessionCreate validation → Database insertion →
SessionRead response → Frontend
```

### **2. AI Analysis Flow**

```
User Data → POST /api/insights/generate → insights.py router →
Fetch recent sessions → GeminiService.generate_insights() →
AI processing → Structured insights → Database storage →
InsightRead response → Frontend
```

### **3. Audio Processing Flow**

```
Audio Upload → POST /api/sessions/{id}/audio → sessions.py router →
File validation → WhisperService.transcribe_audio() →
Text extraction → Optional mistake analysis →
Response with transcription → Frontend
```

---

## 🏛️ **Architectural Patterns Used**

### **1. Layered Architecture**

- **Presentation Layer**: FastAPI routers (API endpoints)
- **Business Logic Layer**: Services package (AI processing)
- **Data Access Layer**: SQLModel models and database.py
- **Database Layer**: Supabase PostgreSQL

### **2. Dependency Injection**

- FastAPI's `Depends()` for database sessions
- Authentication dependencies
- Service layer injection

### **3. Repository Pattern**

- SQLModel handles database abstractions
- Clean separation between models and business logic

### **4. Strategy Pattern**

- Different AI services (Gemini, Whisper) implementing common interface
- Interchangeable AI providers

### **5. DTO (Data Transfer Object) Pattern**

- Separate Create/Read/Update schemas
- Input validation and output formatting

---

## 🔐 **Security Architecture**

### **Database Security**

- Row Level Security (RLS) policies
- User isolation at database level
- Foreign key constraints

### **API Security**

- JWT authentication (placeholder ready)
- Input validation with Pydantic
- CORS configuration
- File upload restrictions

### **AI Service Security**

- API key management
- Rate limiting
- Error message sanitization
- Input size restrictions

---

## 📊 **Database Schema Relationships**

```
Users (Supabase Auth)
    ↓ (one-to-many)
Sessions
    ↓ (one-to-many)
├── PortionDetails
├── Mistakes
├── TestTypes
└── LearningMethods

Users (Supabase Auth)
    ↓ (one-to-many)
Insights
```

This architecture provides:

- **Scalability**: Modular services and clean separation
- **Maintainability**: Clear file organization and responsibilities
- **Testability**: Dependency injection and isolated components
- **Extensibility**: Easy to add new AI services or endpoints
- **Security**: Multi-layer protection and validation

Would you like me to explain any specific part in more detail?
