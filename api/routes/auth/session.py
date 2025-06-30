from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

# Import database session operations
from database.operations.session_operations import (
    create_session as db_create_session,
    get_session as db_get_session,
    get_user_from_session,
    update_session_access as db_update_session_access,
    invalidate_session as db_invalidate_session
)
from database.models.session import Session
from database.models.user import User

def create_session(user_id: int) -> Optional[str]:
    """Create a new session for the user in the database"""
    return db_create_session(user_id)

def get_session(session_id: str) -> Optional[Session]:
    """Get session data from the database"""
    return db_get_session(session_id)

def is_session_expired(session: Session) -> bool:
    """Check if session is expired"""
    if not session:
        return True
    
    return session.is_expired()

def is_session_valid(session: Session) -> bool:
    """Check if session is valid (active and not expired)"""
    if not session:
        return False
    
    return session.is_valid()

def update_session_access(session_id: str) -> bool:
    """Update last accessed time for session"""
    return db_update_session_access(session_id)

def invalidate_session(session_id: str) -> bool:
    """Invalidate session in database"""
    return db_invalidate_session(session_id)
