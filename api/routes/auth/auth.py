from fastapi import APIRouter, Request, HTTPException, Response, Depends
from fastapi.responses import RedirectResponse
from typing import Dict, Any
from sqlalchemy.orm import Session
import os
import httpx
import secrets
import json
from datetime import datetime, timedelta
from .session import get_session, is_session_valid, update_session_access
from database.connection import get_db
from database.operations.user_operations import (
    get_user_by_id
)
from database.operations.session_operations import get_user_from_session
from database.models.user import UserStatus

router = APIRouter()


@router.get("/me")
async def get_current_user(request: Request):
    """
    Check if user is authenticated and return user data
    """
    session_id = request.cookies.get("session_id")
    
    # Is there a session?
    if not session_id:
        return {
            "authenticated": False,
            "message": "No session found."
        }
    
    # If yes, is it valid?
    session = get_session(session_id)
    if not session or not is_session_valid(session):
        return {
            "authenticated": False,
            "message": "Session expired or invalid."
        }
    
    # Is there a user associated with the session? Get from db
    user = get_user_from_session(session_id)
    if not user:
        return {
            "authenticated": False,
            "message": "User not found."
        }
    
    # Update session last accessed time
    update_session_access(session_id)
    
    # Return the user data
    return {
        "authenticated": True,
        "user": {
            "id": user.id,
            "discord_username": user.discord_username,
            "status": user.status.value  # UserStatus is an enum, so we need .value
        }
    }


@router.post("/logout")
async def logout(request: Request, response: Response):
    """
    Logout user by clearing session
    """
    session_id = request.cookies.get("session_id")
    
    # Invalidate session in storage
    if session_id:
        from .session import invalidate_session
        invalidate_session(session_id)
    
    # Clear the session cookie
    response.delete_cookie("session_id")
    
    return {"message": "Logged out successfully"}
