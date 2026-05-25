import enum
from sqlalchemy import Column, String, Integer, Enum as SQLEnum
from app.db.database import Base

class DepartmentEnum(str, enum.Enum):
    ENGINEERING = "Engineering"
    SALES = "Sales"
    HR = "HR"

class Employee(Base):
    __tablename__ = "employees"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    department = Column(SQLEnum(DepartmentEnum), nullable=False)
    salary = Column(Integer, nullable=False)