from pydantic import BaseModel, EmailStr, ConfigDict
from enum import Enum
from typing import Optional
from datetime import datetime


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


class EmployeeUpdate(BaseModel):
    """All fields optional — supports partial (PATCH-style) updates via PUT."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[DepartmentEnum] = None
    salary: Optional[int] = None


class EmployeeResponse(EmployeeBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
