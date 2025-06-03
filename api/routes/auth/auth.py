from fastapi import APIRouter, Request, HTTPException, Response
from fastapi.responses import RedirectResponse
from typing import Dict, Any
import os
import httpx
import secrets
import json
from datetime import datetime, timedelta
from .session import get_session, is_session_expired, update_session_access

router = APIRouter()

# Placeholder functions - you'll implement these later


def get_user_by_id(user_id: int) -> Dict[str, Any] | None:
    """Get user from database"""
    # TODO: Implement user lookup
    return None


def store_user_pending_approval(user_data: Dict[str, Any]) -> None:
    """Store user data pending admin approval"""
    # TODO: Implement user storage in database with 'pending' status
    pass

def get_user_by_discord_id(discord_id: str) -> Dict[str, Any] | None:
    """Get user by Discord ID"""
    # TODO: Implement user lookup by Discord ID
    return None

def is_user_approved(user: Dict[str, Any]) -> bool:
    """Check if user is approved by admin"""
    # TODO: Check user status in database
    return user.get("status") == "approved"


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
    if not session or is_session_expired(session):
        return {
            "authenticated": False,
            "message": "Session expired or invalid."
        }
    
    # Is there a user associated with the session? Get from db
    user = get_user_by_id(session.get("user_id"))
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
            "id": user["id"],
            "discord_username": user["discord_username"],
            "discord_avatar": user["discord_avatar"],
            "status": user["status"]
        }
    }


@router.post("/logout")
async def logout(response: Response):
    """
    Logout user by clearing session
    """
    # Clear the session cookie
    response.delete_cookie("session_id")
    
    # TODO: Invalidate session in storage (Redis/DB)
    
    return {"message": "Logged out successfully"}
