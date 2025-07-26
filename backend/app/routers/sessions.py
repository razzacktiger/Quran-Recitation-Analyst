"""
Sessions router for managing Quran practice sessions
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlmodel import Session, select
from typing import List, Dict, Any, Optional
import os

from app.database import get_db
from app.models.sessions import Session as SessionModel, SessionCreate, SessionRead, SessionUpdate
from app.models.mistakes import Mistake, MistakeCreate
from app.models.portion_details import PortionDetail, PortionDetailCreate
from app.routers.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=SessionRead)
async def create_session(
    session_data: SessionCreate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create a new Quran practice session"""
    try:
        # Create session with user ID
        session = SessionModel(
            user_id=current_user["id"],
            **session_data.model_dump()
        )
        
        db.add(session)
        db.commit()
        db.refresh(session)
        
        return session
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating session: {str(e)}"
        )

@router.get("/", response_model=List[SessionRead])
async def get_user_sessions(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get all sessions for the current user"""
    try:
        statement = (
            select(SessionModel)
            .where(SessionModel.user_id == current_user["id"])
            .order_by(SessionModel.timestamp.desc())
            .offset(offset)
            .limit(limit)
        )
        
        sessions = db.exec(statement).all()
        return sessions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching sessions: {str(e)}"
        )

@router.get("/{session_id}", response_model=SessionRead)
async def get_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get a specific session by ID"""
    try:
        statement = select(SessionModel).where(
            SessionModel.id == session_id,
            SessionModel.user_id == current_user["id"]
        )
        
        session = db.exec(statement).first()
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        return session
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching session: {str(e)}"
        )

@router.put("/{session_id}", response_model=SessionRead)
async def update_session(
    session_id: int,
    session_update: SessionUpdate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Update a session"""
    try:
        statement = select(SessionModel).where(
            SessionModel.id == session_id,
            SessionModel.user_id == current_user["id"]
        )
        
        session = db.exec(statement).first()
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Update fields
        update_data = session_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(session, field, value)
        
        db.add(session)
        db.commit()
        db.refresh(session)
        
        return session
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating session: {str(e)}"
        )

@router.delete("/{session_id}")
async def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Delete a session"""
    try:
        statement = select(SessionModel).where(
            SessionModel.id == session_id,
            SessionModel.user_id == current_user["id"]
        )
        
        session = db.exec(statement).first()
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        db.delete(session)
        db.commit()
        
        return {"message": "Session deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting session: {str(e)}"
        )

@router.post("/{session_id}/mistakes")
async def add_mistake_to_session(
    session_id: int,
    mistake_data: MistakeCreate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Add a mistake to a session"""
    try:
        # Verify session belongs to user
        session_statement = select(SessionModel).where(
            SessionModel.id == session_id,
            SessionModel.user_id == current_user["id"]
        )
        
        session = db.exec(session_statement).first()
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Create mistake
        mistake = Mistake(session_id=session_id, **mistake_data.model_dump())
        db.add(mistake)
        db.commit()
        db.refresh(mistake)
        
        return mistake
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding mistake: {str(e)}"
        )

@router.post("/{session_id}/portions")
async def add_portion_to_session(
    session_id: int,
    portion_data: PortionDetailCreate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Add portion details to a session"""
    try:
        # Verify session belongs to user
        session_statement = select(SessionModel).where(
            SessionModel.id == session_id,
            SessionModel.user_id == current_user["id"]
        )
        
        session = db.exec(session_statement).first()
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Create portion detail
        portion = PortionDetail(session_id=session_id, **portion_data.model_dump())
        db.add(portion)
        db.commit()
        db.refresh(portion)
        
        return portion
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding portion: {str(e)}"
        )

@router.post("/{session_id}/audio")
async def upload_session_audio(
    session_id: int,
    audio_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Upload audio file for a session
    TODO: Integrate with Whisper API for transcription
    """
    try:
        # Verify session belongs to user
        session_statement = select(SessionModel).where(
            SessionModel.id == session_id,
            SessionModel.user_id == current_user["id"]
        )
        
        session = db.exec(session_statement).first()
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Validate file type
        allowed_types = ["audio/mpeg", "audio/wav", "audio/m4a", "audio/ogg"]
        if audio_file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type. Allowed: {allowed_types}"
            )
        
        # For now, just return success message
        # TODO: Implement audio processing with Whisper
        return {
            "message": "Audio uploaded successfully",
            "filename": audio_file.filename,
            "size": audio_file.size,
            "content_type": audio_file.content_type,
            "session_id": session_id,
            "note": "Audio processing will be implemented with Whisper API"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading audio: {str(e)}"
        ) 