from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, Dict, Any
from ...models.user import User, UserStatus
from ...connection import SessionLocal

def get_user_by_id(user_id: int) -> Optional[User]:
    """
    Get a user by their ID
    Params: user_id (int): The ID of the user to retrieve
    Returns: User | None: The user object if found, otherwise None
    """
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        return user
    except Exception as e:
        print(f"Error retrieving user by ID {user_id}: {e}")
    finally:
        db.close()