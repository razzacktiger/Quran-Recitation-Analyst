"""
Portion details model for tracking Quran portions studied
"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum


class RecencyCategory(str, Enum):
    """Recency categories for portion review"""
    NEW = "new"
    RECENT = "recent"
    REVIEWING = "reviewing"
    MAINTENANCE = "maintenance"


class PortionDetailBase(SQLModel):
    """Base portion detail model"""
    session_id: int = Field(foreign_key="sessions.id", description="Session ID")
    portion_type: str = Field(description="Type of portion (surah, ayah, juz)")
    reference: str = Field(description="Portion reference (e.g., 'Al-Fatiha', '2:1-10')")
    recency_category: Optional[RecencyCategory] = Field(default=None, description="Review recency category")


class PortionDetail(PortionDetailBase, table=True):
    """Portion detail database model"""
    __tablename__ = "portion_details"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    
    # Relationships
    session: Optional["Session"] = Relationship(back_populates="portion_details")


class PortionDetailCreate(PortionDetailBase):
    """Schema for creating portion detail"""
    pass


class PortionDetailRead(PortionDetailBase):
    """Schema for reading portion detail"""
    id: int
    created_at: datetime


class PortionDetailUpdate(SQLModel):
    """Schema for updating portion detail"""
    portion_type: Optional[str] = None
    reference: Optional[str] = None
    recency_category: Optional[RecencyCategory] = None 