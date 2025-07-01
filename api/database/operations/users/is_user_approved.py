from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, Dict, Any
from ...models.user import User, UserStatus
from ...connection import SessionLocal

def is_user_approved(user: User) -> bool:
    """
    Check if user is approved by admin
    Params: user (User): The user object to check
    Returns: bool: True if user is approved, False otherwise
    """
    try:
        if user and user.status == UserStatus.APPROVED:
            return True
        return False
    except Exception as e:
        print(f"Error checking user approval status: {e}")
        return False