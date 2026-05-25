import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import Base
from app.api.dependencies import get_db

# 1. USE A SEPARATE TEST DATABASE (Crucial for Apex Quality)
# This prevents your tests from wiping out your 'real' dev data.
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db" # Using SQLite for speed in tests

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for every single test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine) # Wipe it clean

@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client that uses the override_get_db dependency."""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    # This is the "Magic": We swap the real DB for the Test DB during the test
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()