from .connection import engine, Base
from .models import User, Session  # Import models to register them with Base

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def drop_tables():
    """Drop all database tables (use with caution!)"""
    Base.metadata.drop_all(bind=engine)
    print("Database tables dropped!")

if __name__ == "__main__":
    create_tables()

