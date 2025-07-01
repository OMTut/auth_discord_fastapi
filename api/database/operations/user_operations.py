from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, Dict, Any
from ..models.user import User, UserStatus
from ..connection import SessionLocal

def store_user_pending_approval(user_data: Dict[str, Any]) -> Optional[User]:
    """
    Store user data pending admin approval
    Params: user_data (Dict[str, Any]): The user data to store
    Returns: Optional[User]: The created user object if successful, None otherwise
    """
    db: Session = SessionLocal()
    try:
        user = User(
            discord_id=user_data.get("id"),
            discord_username=user_data.get("username"),
            server_nickname=user_data.get("server_nickname"),  # Include server nickname
            email=user_data.get("email"),
            status=UserStatus.PENDING
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as e:
        db.rollback()
        print(f"Integrity error storing user pending approval: {e.orig}")
        return None
    except Exception as e:
        db.rollback()
        print(f"Error storing user pending approval: {e}")
        return None
    finally:
        db.close()

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
