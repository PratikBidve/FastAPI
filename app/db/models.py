import enum
from sqlalchemy import Column, String, Integer, Enum as SQLEnum, DateTime, func
from app.db.database import Base
from ..schemas.employee import DepartmentEnum

class Employee(Base):
    __tablename__ = "employees"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    department = Column(SQLEnum(DepartmentEnum), nullable=False)
    salary = Column(Integer, nullable=False)

    # Audit timestamps — server-side defaults, never set manually
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
