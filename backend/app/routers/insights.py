"""
Insights router for AI-generated coaching insights
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Dict, Any
from datetime import datetime, timedelta

from app.database import get_db
from app.models.insights import Insight, InsightCreate, InsightRead, InsightUpdate
from app.models.sessions import Session as SessionModel
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[InsightRead])
async def get_user_insights(
    limit: int = 10,
    offset: int = 0,
    insight_type: str = None,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get AI insights for the current user"""
    try:
        statement = (
            select(Insight)
            .where(Insight.user_id == current_user["id"])
            .order_by(Insight.generated_at.desc())
        )
        
        # Filter by insight type if provided
        if insight_type:
            statement = statement.where(Insight.insight_type == insight_type)
        
        # Apply pagination
        statement = statement.offset(offset).limit(limit)
        
        insights = db.exec(statement).all()
        return insights
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching insights: {str(e)}"
        )

@router.get("/{insight_id}", response_model=InsightRead)
async def get_insight(
    insight_id: int,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get a specific insight by ID"""
    try:
        statement = select(Insight).where(
            Insight.id == insight_id,
            Insight.user_id == current_user["id"]
        )
        
        insight = db.exec(statement).first()
        if not insight:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Insight not found"
            )
        
        return insight
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching insight: {str(e)}"
        )

@router.post("/generate", response_model=InsightRead)
async def generate_insight(
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Generate new AI insights based on recent session data
    TODO: Integrate with Gemini AI for analysis
    """
    try:
        # Get recent sessions for analysis
        recent_date = datetime.now() - timedelta(days=7)
        sessions_statement = (
            select(SessionModel)
            .where(
                SessionModel.user_id == current_user["id"],
                SessionModel.timestamp >= recent_date
            )
            .order_by(SessionModel.timestamp.desc())
        )
        
        recent_sessions = db.exec(sessions_statement).all()
        
        if not recent_sessions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No recent sessions found for analysis"
            )
        
        # Placeholder insight generation
        # TODO: Replace with actual Gemini AI integration
        insight_data = {
            "user_id": current_user["id"],
            "summary": f"Based on {len(recent_sessions)} recent sessions, you're making good progress! Consider focusing on consistent daily practice.",
            "next_actions": {
                "recommendations": [
                    "Practice for 15-20 minutes daily",
                    "Focus on problematic verses identified in recent sessions",
                    "Use repetition method for memorization"
                ],
                "review_schedule": {
                    "next_review": (datetime.now() + timedelta(days=1)).isoformat(),
                    "priority_portions": ["Al-Fatiha", "Last 3 Surahs"]
                }
            },
            "confidence_score": 0.85,
            "insight_type": "general",
            "expires_at": datetime.now() + timedelta(days=7)
        }
        
        # Create insight
        insight = Insight(**insight_data)
        db.add(insight)
        db.commit()
        db.refresh(insight)
        
        return insight
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating insight: {str(e)}"
        )

@router.get("/stats/overview")
async def get_user_stats(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get user statistics overview"""
    try:
        # Get sessions from the last N days
        recent_date = datetime.now() - timedelta(days=days)
        sessions_statement = (
            select(SessionModel)
            .where(
                SessionModel.user_id == current_user["id"],
                SessionModel.timestamp >= recent_date
            )
        )
        
        sessions = db.exec(sessions_statement).all()
        
        if not sessions:
            return {
                "total_sessions": 0,
                "total_duration": 0,
                "average_score": 0,
                "sessions_this_week": 0,
                "improvement_trend": "No data"
            }
        
        # Calculate statistics
        total_sessions = len(sessions)
        total_duration = sum(s.duration or 0 for s in sessions)
        scores = [s.performance_score for s in sessions if s.performance_score is not None]
        average_score = sum(scores) / len(scores) if scores else 0
        
        # Sessions this week
        week_ago = datetime.now() - timedelta(days=7)
        sessions_this_week = len([s for s in sessions if s.timestamp >= week_ago])
        
        return {
            "total_sessions": total_sessions,
            "total_duration": total_duration,
            "average_score": round(average_score, 2),
            "sessions_this_week": sessions_this_week,
            "improvement_trend": "Improving" if average_score > 70 else "Needs focus",
            "period_days": days
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching stats: {str(e)}"
        )

@router.put("/{insight_id}", response_model=InsightRead)
async def update_insight(
    insight_id: int,
    insight_update: InsightUpdate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Update an insight"""
    try:
        statement = select(Insight).where(
            Insight.id == insight_id,
            Insight.user_id == current_user["id"]
        )
        
        insight = db.exec(statement).first()
        if not insight:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Insight not found"
            )
        
        # Update fields
        update_data = insight_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(insight, field, value)
        
        db.add(insight)
        db.commit()
        db.refresh(insight)
        
        return insight
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating insight: {str(e)}"
        )

@router.delete("/{insight_id}")
async def delete_insight(
    insight_id: int,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Delete an insight"""
    try:
        statement = select(Insight).where(
            Insight.id == insight_id,
            Insight.user_id == current_user["id"]
        )
        
        insight = db.exec(statement).first()
        if not insight:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Insight not found"
            )
        
        db.delete(insight)
        db.commit()
        
        return {"message": "Insight deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting insight: {str(e)}"
        ) 