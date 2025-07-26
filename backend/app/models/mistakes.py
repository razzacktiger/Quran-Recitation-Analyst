"""
Mistake model for tracking Quran recitation errors
"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum


class ResolutionStatus(str, Enum):
    """Resolution status for mistakes"""
    PENDING = "pending"
    PRACTICING = "practicing"
    RESOLVED = "resolved"


class MistakeBase(SQLModel):
    """Base mistake model"""
    session_id: int = Field(foreign_key="sessions.id", description="Session ID")
    location: str = Field(description="Error location (e.g., 'Surah 2, Ayah 5, Word 3')")
    error_category: str = Field(description="Error category (pronunciation, memorization, tajweed)")
    error_subcategory: Optional[str] = Field(default=None, description="Error subcategory (makhraj, sifat, word_order)")
    details: Optional[str] = Field(default=None, description="Detailed description of the mistake")
    correction_method: Optional[str] = Field(default=None, description="Suggested correction method")
    resolution_status: ResolutionStatus = Field(default=ResolutionStatus.PENDING, description="Resolution status")
    severity_level: int = Field(default=1, ge=1, le=5, description="Severity level (1-5)")


class Mistake(MistakeBase, table=True):
    """Mistake database model"""
    __tablename__ = "mistakes"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = Field(default=None, description="When the mistake was resolved")
    
    # Relationships
    session: Optional["Session"] = Relationship(back_populates="mistakes")


class MistakeCreate(MistakeBase):
    """Schema for creating mistake"""
    pass


class MistakeRead(MistakeBase):
    """Schema for reading mistake"""
    id: int
    created_at: datetime
    resolved_at: Optional[datetime] = None


class MistakeUpdate(SQLModel):
    """Schema for updating mistake"""
    error_category: Optional[str] = None
    error_subcategory: Optional[str] = None
    details: Optional[str] = None
    correction_method: Optional[str] = None
    resolution_status: Optional[ResolutionStatus] = None
    severity_level: Optional[int] = Field(default=None, ge=1, le=5)
    resolved_at: Optional[datetime] = None 