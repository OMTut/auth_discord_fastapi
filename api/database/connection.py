from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
import pathlib

# Load .env file from the api directory
env_path = pathlib.Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

# Database dependency for FastAPI
def get_db():
    """
    FastAPI dependency to get database session
    Open per request and close when done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test the database connection
def test_db_connection():
    """
    Test the database connection
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connected successfully!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

