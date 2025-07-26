"""
Test type model for tracking different testing methods
"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class TestTypeBase(SQLModel):
    """Base test type model"""
    session_id: int = Field(foreign_key="sessions.id", description="Session ID")
    category: str = Field(description="Test category (recitation, memorization, revision)")
    description: Optional[str] = Field(default=None, description="Test description")
    success_rate: Optional[float] = Field(default=None, ge=0, le=100, description="Success rate percentage")


class TestType(TestTypeBase, table=True):
    """Test type database model"""
    __tablename__ = "test_types"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    
    # Relationships
    session: Optional["Session"] = Relationship(back_populates="test_types")


class TestTypeCreate(TestTypeBase):
    """Schema for creating test type"""
    pass


class TestTypeRead(TestTypeBase):
    """Schema for reading test type"""
    id: int
    created_at: datetime


class TestTypeUpdate(SQLModel):
    """Schema for updating test type"""
    category: Optional[str] = None
    description: Optional[str] = None
    success_rate: Optional[float] = Field(default=None, ge=0, le=100) 