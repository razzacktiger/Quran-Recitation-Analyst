"""
Insight model for AI-generated coaching insights
"""

from datetime import datetime
from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field, JSON
from enum import Enum


class InsightType(str, Enum):
    """Types of insights"""
    GENERAL = "general"
    WEAKNESS_FOCUS = "weakness_focus"
    STRENGTH_REINFORCEMENT = "strength_reinforcement"
    REVIEW_SCHEDULE = "review_schedule"


class InsightBase(SQLModel):
    """Base insight model"""
    user_id: str = Field(description="User identifier")
    summary: str = Field(description="Insight summary")
    next_actions: Optional[Dict[str, Any]] = Field(default=None, sa_type=JSON, description="Structured recommendations and review schedule")
    confidence_score: Optional[float] = Field(default=None, ge=0, le=1, description="AI confidence score (0-1)")
    insight_type: InsightType = Field(default=InsightType.GENERAL, description="Type of insight")
    expires_at: Optional[datetime] = Field(default=None, description="When this insight becomes stale")


class Insight(InsightBase, table=True):
    """Insight database model"""
    __tablename__ = "insights"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    generated_at: Optional[datetime] = Field(default_factory=datetime.now, description="When insight was generated")


class InsightCreate(InsightBase):
    """Schema for creating insight"""
    pass


class InsightRead(InsightBase):
    """Schema for reading insight"""
    id: int
    generated_at: datetime


class InsightUpdate(SQLModel):
    """Schema for updating insight"""
    summary: Optional[str] = None
    next_actions: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = Field(default=None, ge=0, le=1)
    insight_type: Optional[InsightType] = None
    expires_at: Optional[datetime] = None 