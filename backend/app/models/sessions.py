"""
Session model for Quran practice sessions
"""

from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class SessionBase(SQLModel):
    """Base session model with common fields"""
    user_id: str = Field(description="User identifier")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="Session timestamp")
    duration: Optional[int] = Field(default=None, description="Session duration in minutes")
    performance_score: Optional[float] = Field(
        default=None, 
        ge=0, 
        le=100, 
        description="Performance score (0-100)"
    )
    notes: Optional[str] = Field(default=None, description="Additional session notes")


class Session(SessionBase, table=True):
    """Session database model"""
    __tablename__ = "sessions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    
    # Relationships
    portion_details: List["PortionDetail"] = Relationship(back_populates="session")
    mistakes: List["Mistake"] = Relationship(back_populates="session") 
    test_types: List["TestType"] = Relationship(back_populates="session")
    learning_methods: List["LearningMethod"] = Relationship(back_populates="session")


class SessionCreate(SessionBase):
    """Schema for creating a new session"""
    pass


class SessionRead(SessionBase):
    """Schema for reading session data"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    # Optional: Include related data
    portion_details: Optional[List["PortionDetailRead"]] = None
    mistakes: Optional[List["MistakeRead"]] = None
    test_types: Optional[List["TestTypeRead"]] = None
    learning_methods: Optional[List["LearningMethodRead"]] = None


class SessionUpdate(SQLModel):
    """Schema for updating session data"""
    duration: Optional[int] = None
    performance_score: Optional[float] = Field(default=None, ge=0, le=100)
    notes: Optional[str] = None


# Forward references for relationships
from .portion_details import PortionDetailRead
from .mistakes import MistakeRead
from .test_types import TestTypeRead
from .learning_methods import LearningMethodRead

SessionRead.model_rebuild() 