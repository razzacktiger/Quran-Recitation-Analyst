"""
Learning method model for tracking different learning approaches
"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class LearningMethodBase(SQLModel):
    """Base learning method model"""
    session_id: int = Field(foreign_key="sessions.id", description="Session ID")
    method_type: str = Field(description="Method type (repetition, visualization, audio)")
    details: Optional[str] = Field(default=None, description="Method details")
    effectiveness_rating: Optional[int] = Field(default=None, ge=1, le=5, description="Effectiveness rating (1-5)")


class LearningMethod(LearningMethodBase, table=True):
    """Learning method database model"""
    __tablename__ = "learning_methods"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    
    # Relationships
    session: Optional["Session"] = Relationship(back_populates="learning_methods")


class LearningMethodCreate(LearningMethodBase):
    """Schema for creating learning method"""
    pass


class LearningMethodRead(LearningMethodBase):
    """Schema for reading learning method"""
    id: int
    created_at: datetime


class LearningMethodUpdate(SQLModel):
    """Schema for updating learning method"""
    method_type: Optional[str] = None
    details: Optional[str] = None
    effectiveness_rating: Optional[int] = Field(default=None, ge=1, le=5) 