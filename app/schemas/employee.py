from pydantic import BaseModel, EmailStr, ConfigDict
from enum import Enum

class DepartmentEnum(str, Enum):
    ENGINEERING = "Engineering"
    SALES = "Sales"
    HR = "HR"

class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    department: DepartmentEnum
    salary: int

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: str
    
    # This tells Pydantic to treat SQLAlchemy objects as dicts
    model_config = ConfigDict(from_attributes=True)