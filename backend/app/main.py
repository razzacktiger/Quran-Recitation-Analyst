"""
AI-Powered Quran Coach FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv

from app.database import engine, create_db_and_tables
from app.routers import sessions, insights, auth

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application lifespan events"""
    # Startup
    print("🔄 Attempting database connection...")
    try:
        create_db_and_tables()
        print("✅ Database tables created successfully")
        print("✅ Supabase connection working!")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        print("⚠️ Continuing without database - check credentials in .env")
    
    yield
    
    # Shutdown (if needed in the future)
    print("🔄 Application shutting down...")

app = FastAPI(
    title="AI-Powered Quran Coach API",
    description="Backend API for Quran memorization and recitation coaching with AI insights",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(sessions.router, prefix="/api/sessions", tags=["sessions"])
app.include_router(insights.router, prefix="/api/insights", tags=["insights"])



@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI-Powered Quran Coach API",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        from app.database import get_db
        
        return {
            "status": "healthy",
            "service": "quran-coach-api",
            "database": "connected",
            "timestamp": "2025-01-17T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service unhealthy: {str(e)}"
        )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if os.getenv("DEBUG") == "True" else "Something went wrong"
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "True") == "True"
    ) 