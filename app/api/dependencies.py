from typing import Generator
from app.db.database import SessionLocal

def get_db() -> Generator:
    """
    Dependency that creates a new SQLAlchemy session for each request
    and ensures it is closed after the request is processed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()