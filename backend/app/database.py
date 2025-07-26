"""
Database configuration and connection management
Handles Supabase PostgreSQL connection and SQLModel setup
"""

import os
from typing import Generator
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Construct from Supabase components if DATABASE_URL not provided
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    if SUPABASE_URL:
        # Extract connection details from Supabase URL
        # Format: https://project-id.supabase.co
        project_id = SUPABASE_URL.replace("https://", "").replace(".supabase.co", "")
        DATABASE_URL = f"postgresql://postgres:your-password@db.{project_id}.supabase.co:5432/postgres"

if not DATABASE_URL:
    raise ValueError("DATABASE_URL must be set in environment variables")

# Create database engine
engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("DEBUG", "False") == "True",  # Log SQL queries in debug mode
    pool_pre_ping=True,  # Validate connections before use
    pool_recycle=3600,   # Recycle connections every hour
)

def create_db_and_tables():
    """Create database tables based on SQLModel models"""
    try:
        # Import all models to ensure they're registered
        from app.models.sessions import Session as SessionModel
        from app.models.insights import Insight
        from app.models.mistakes import Mistake
        from app.models.portion_details import PortionDetail
        from app.models.test_types import TestType
        from app.models.learning_methods import LearningMethod
        
        SQLModel.metadata.create_all(engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        raise

def get_db() -> Generator[Session, None, None]:
    """
    Database dependency for FastAPI
    Provides database session for each request
    """
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

# Test database connection
def test_connection():
    """Test database connectivity"""
    try:
        with Session(engine) as session:
            # Simple query to test connection
            result = session.execute("SELECT 1")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    # Test connection when run directly
    if test_connection():
        print("✅ Database connection successful")
    else:
        print("❌ Database connection failed") 