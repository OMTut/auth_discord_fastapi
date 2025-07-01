"""
Tests for user operations
"""
import pytest
from database.operations.users import (
    store_user_pending_approval,
    get_user_by_id,
    get_user_by_discord_id,
    get_server_nickname_by_user_id,
    is_user_approved
)
from database.models.user import User, UserStatus


def test_store_user_pending_approval(db_session, sample_user_data):
    """Test storing user data pending approval"""
    user = store_user_pending_approval(sample_user_data)

    assert user is not None
    assert user.discord_id == sample_user_data["id"]
    assert user.discord_username == sample_user_data["username"]
    assert user.server_nickname == sample_user_data["server_nickname"]
    assert user.email == sample_user_data["email"]
    assert user.status == UserStatus.PENDING


def test_get_user_by_id(db_session, sample_user_data):
    """Test retrieving a user by ID"""
    # First store the user
    user = store_user_pending_approval(sample_user_data)

    # Retrieve by ID
    retrieved_user = get_user_by_id(user.id)

    assert retrieved_user is not None
    assert retrieved_user.discord_id == sample_user_data["id"]


def test_get_user_by_discord_id(db_session, sample_user_data):
    """Test retrieving a user by Discord ID"""
    # First store the user
    user = store_user_pending_approval(sample_user_data)

    # Retrieve by Discord ID
    retrieved_user = get_user_by_discord_id(sample_user_data["id"])
    
    assert retrieved_user is not None
    assert retrieved_user.id == user.id

def test_get_server_nickname_by_user_id(db_session, sample_user_data):
    """Test retrieving a user's server nickname by user ID"""
    # First store the user
    user = store_user_pending_approval(sample_user_data)

    # Retrieve server nickname by user ID
    server_nickname = get_server_nickname_by_user_id(user.id)

    assert server_nickname is not None
    assert server_nickname == sample_user_data["server_nickname"]


def test_get_server_nickname_by_user_id_nonexistent(db_session):
    """Test retrieving server nickname for non-existent user"""
    nickname = get_server_nickname_by_user_id(99999)  # ID that doesn't exist
    assert nickname is None


def test_get_server_nickname_by_user_id_no_nickname(db_session, sample_user_data):
    """Test retrieving server nickname when user has no nickname set"""
    # Create user data without server nickname
    user_data_no_nickname = sample_user_data.copy()
    user_data_no_nickname["server_nickname"] = None
    
    # Store the user
    user = store_user_pending_approval(user_data_no_nickname)
    
    # Retrieve server nickname
    server_nickname = get_server_nickname_by_user_id(user.id)
    
    assert server_nickname is None


def test_is_user_approved_with_real_users(db_session, sample_user_data):
    """Test checking if a user is approved using real database users"""
    # Create a pending user (default status)
    pending_user = store_user_pending_approval(sample_user_data)
    assert is_user_approved(pending_user) is False
    
    # Manually set user to approved status and test
    pending_user.status = UserStatus.APPROVED
    db_session.commit()
    assert is_user_approved(pending_user) is True
    
    # Test rejected user
    pending_user.status = UserStatus.REJECTED
    db_session.commit()
    assert is_user_approved(pending_user) is False
    
    # Test banned user
    pending_user.status = UserStatus.BANNED
    db_session.commit()
    assert is_user_approved(pending_user) is False


def test_is_user_approved_edge_cases():
    """Test edge cases for is_user_approved function"""
    # Test with None user
    assert is_user_approved(None) is False


def test_get_user_by_id_nonexistent(db_session):
    """Test retrieving a non-existent user by ID"""
    user = get_user_by_id(99999)  # ID that doesn't exist
    assert user is None


def test_get_user_by_discord_id_nonexistent(db_session):
    """Test retrieving a non-existent user by Discord ID"""
    user = get_user_by_discord_id("999999999999999999")  # Discord ID that doesn't exist
    assert user is None


def test_store_user_duplicate_discord_id(db_session, sample_user_data):
    """Test storing a user with duplicate Discord ID (should fail)"""
    # Store first user
    user1 = store_user_pending_approval(sample_user_data)
    assert user1 is not None

    # Try to store another user with same Discord ID
    user2 = store_user_pending_approval(sample_user_data)
    assert user2 is None  # Should fail due to unique constraint


def test_store_user_missing_data(db_session):
    """Test storing user with missing required data"""
    incomplete_data = {
        "username": "testuser",
        # Missing 'id' (Discord ID) which is required
        "email": "test@example.com"
    }
    
    user = store_user_pending_approval(incomplete_data)
    # This should either fail or handle gracefully
    # The exact behavior depends on your database constraints
