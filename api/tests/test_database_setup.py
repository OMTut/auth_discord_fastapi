"""
Test database setup and connection
"""
import pytest
from sqlalchemy import text
from database.models.user import User, UserStatus
from database.models.session import Session


def test_database_connection(db_session):
    """Test that we can connect to the test database."""
    result = db_session.execute(text("SELECT 1 as test_value"))
    row = result.fetchone()
    assert row[0] == 1


def test_user_table_exists(db_session):
    """Test that the users table was created."""
    # Try to query the users table
    result = db_session.execute(text("SELECT COUNT(*) FROM users"))
    count = result.fetchone()[0]
    assert count == 0  # Should be empty initially


def test_session_table_exists(db_session):
    """Test that the sessions table was created."""
    # Try to query the sessions table
    result = db_session.execute(text("SELECT COUNT(*) FROM sessions"))
    count = result.fetchone()[0]
    assert count == 0  # Should be empty initially


def test_create_user(db_session, sample_user_data):
    """Test creating a user in the test database."""
    # Create a user
    user = User(
        discord_id=sample_user_data["id"],
        discord_username=sample_user_data["username"],
        email=sample_user_data["email"],
        status=UserStatus.PENDING
    )
    
    db_session.add(user)
    db_session.commit()
    
    # Verify user was created
    created_user = db_session.query(User).filter(User.discord_id == sample_user_data["id"]).first()
    assert created_user is not None
    assert created_user.discord_username == sample_user_data["username"]
    assert created_user.email == sample_user_data["email"]
    assert created_user.status == UserStatus.PENDING


def test_user_count_after_rollback(db_session):
    """Test that users are cleaned up after each test (due to rollback)."""
    # This should be 0 because the previous test's changes were rolled back
    count = db_session.query(User).count()
    assert count == 0
