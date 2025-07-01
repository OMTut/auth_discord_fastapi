import pytest
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from database.connection import Base
from faker import Faker
from unittest.mock import patch

# Load environment variables
load_dotenv()

# Initialize Faker
fake = Faker()

# Test database configuration
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
if not TEST_DATABASE_URL:
    raise ValueError("TEST_DATABASE_URL environment variable is required for testing")

# Create test database engine and session
test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="session")
def setup_test_database():
    """Set up test database tables before running tests."""
    # Mask the password in the URL for security
    masked_url = TEST_DATABASE_URL
    if '@' in masked_url and ':' in masked_url:
        # Extract just the database name and host for display
        parts = masked_url.split('/')
        db_name = parts[-1] if parts else 'unknown'
        host_part = masked_url.split('@')[-1].split('/')[0] if '@' in masked_url else 'localhost'
        masked_url = f"postgresql://***:***@{host_part}/{db_name}"
    
    print(f"\n🔧 Setting up test database: {masked_url}")
    
    # Test database connection
    try:
        with test_engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Test database connection successful")
    except Exception as e:
        print(f"❌ Test database connection failed: {e}")
        raise
    
    # Create all tables
    try:
        Base.metadata.create_all(bind=test_engine)
        print("✅ Test database tables created successfully")
    except Exception as e:
        print(f"❌ Failed to create test database tables: {e}")
        raise
    
    yield
    
    # Cleanup: Drop all tables after tests
    print("\n🧹 Cleaning up test database")
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def db_session(setup_test_database):
    """Create a database session for a test and patch SessionLocal globally."""
    session = TestSessionLocal()
    
    # Patch SessionLocal at the source - this will affect ALL imports
    with patch('database.connection.SessionLocal') as mock_session_local:
        # Return a fresh session each time SessionLocal() is called
        mock_session_local.return_value = session
        
        try:
            yield session
        finally:
            # Clean up all data after each test
            session.rollback()
            
            # Delete all data from tables
            from database.models.session import Session as SessionModel
            from database.models.user import User
            
            session.query(SessionModel).delete()
            session.query(User).delete()
            session.commit()
            
            session.close()

@pytest.fixture
def sample_user_data():
    """Generate sample user data for testing."""
    return {
        "id": str(fake.random_int(min=100000000000000000, max=999999999999999999)),
        "username": fake.user_name(),
        "server_nickname": fake.user_name(),
        "email": fake.email()
    }
