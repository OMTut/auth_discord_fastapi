from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, Dict, Any
from ...models.user import User, UserStatus
from ...connection import SessionLocal

def get_server_nickname_by_user_id(user_id: int) -> Optional[str]:
    """
    Get the server nickname of a user by their ID
    Params: user_id (int): The ID of the user
    Returns: Optional[str]: The server nickname if found, otherwise None
    """
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return user.server_nickname
        return None
    except Exception as e:
        print(f"Error retrieving server nickname for user ID {user_id}: {e}")
        return None
    finally:
        db.close()