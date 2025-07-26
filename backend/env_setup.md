# Environment Setup for Quran Coach Backend (Updated 2025)

Create a `.env` file in the `backend/` directory with the following variables using the latest API versions and best practices:

```bash
# Database Configuration (Get from Supabase project settings)
DATABASE_URL=postgresql://postgres:your-password@db.kwgvbicofprmlomlgwuj.supabase.co:5432/postgres
SUPABASE_URL=https://kwgvbicofprmlomlgwuj.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-key

# AI Services (Latest 2025 Versions)
# OpenAI API Key - supports latest Whisper-1 and GPT models
OPENAI_API_KEY=your-openai-api-key
# Google Gemini API Key - supports Gemini 2.0 Flash
GEMINI_API_KEY=your-gemini-api-key

# Authentication & Security
SECRET_KEY=your-secret-key-here-generate-random-string-minimum-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Settings
DEBUG=True
PORT=8000
HOST=0.0.0.0
# Enhanced CORS settings for 2025
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,https://yourapp.com

# Audio Processing (Enhanced for 2025)
MAX_AUDIO_SIZE_MB=25  # OpenAI Whisper limit
SUPPORTED_AUDIO_FORMATS=mp3,mp4,mpeg,mpga,m4a,wav,webm,ogg,flac
AUDIO_TEMP_DIR=/tmp/quran_audio

# Performance & Rate Limiting (New in 2025)
REQUEST_RATE_LIMIT=100
ASYNC_POOL_SIZE=10
DATABASE_POOL_SIZE=20
```

## Getting Your Supabase Credentials

1. Go to your Supabase project: https://supabase.com/dashboard/project
2. Navigate to **Settings** → **API**
3. Copy the following:
   - **Project URL** → SUPABASE_URL
   - **anon public** key → SUPABASE_KEY
   - **service_role** key → SUPABASE_SERVICE_KEY
4. For DATABASE_URL, go to **Settings** → **Database** and copy the connection string

## Getting AI API Keys

### OpenAI (for Whisper)

1. Visit: https://platform.openai.com/api-keys
2. Create a new API key
3. Add it as OPENAI_API_KEY

### Gemini (for Text Analysis)

1. Visit: https://makersuite.google.com/app/apikey
2. Create a new API key
3. Add it as GEMINI_API_KEY

## Generate Secret Key

Run this Python command to generate a secure secret key:

```python
import secrets
print(secrets.token_urlsafe(32))
```

## Testing Your Setup

Once configured, test the backend:

```bash
cd backend
pip install -r requirements.txt
python -m app.main
```

Visit http://localhost:8000/docs to see the API documentation!
