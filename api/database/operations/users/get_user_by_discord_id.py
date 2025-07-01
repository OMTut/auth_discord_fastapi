from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, Dict, Any
from ...models.user import User, UserStatus
from ...connection import SessionLocal

def get_user_by_discord_id(discord_id: str) -> Optional[User]:
    """
    Get a user by their Discord ID
    Params: discord_id (str): The Discord ID of the user to retrieve
    Returns: Optional[User]: The user object if found, otherwise None
    """
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.discord_id == discord_id).first()
        return user
    finally:
        db.close()