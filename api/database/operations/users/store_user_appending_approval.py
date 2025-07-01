from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, Dict, Any
from ...models.user import User, UserStatus
from ...connection import SessionLocal


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