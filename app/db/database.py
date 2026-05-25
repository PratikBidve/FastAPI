from sqlalchemy.engine.base import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Notice how we no longer hardcode the URL here. 
# We pull the validated URI from Pydantic.
engine: Engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()