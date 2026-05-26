from sqlalchemy.engine.base import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Notice how we no longer hardcode the URL here. 
# We pull the validated URI from Pydantic.
engine: Engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    pool_pre_ping=True,    # Verifies connection health before querying
    pool_size=10,          # Pre-allocates 10 sockets
    max_overflow=20        # Allows 20 more under heavy traffic
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()