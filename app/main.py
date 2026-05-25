from fastapi import FastAPI
from app.api.v1 import employees
from app.core.config import settings

# Initialize the App with Metadata from Config
app = FastAPI(
    title=settings.PROJECT_NAME, 
    version=settings.VERSION,
    description="Enterprise Grade HCM API for ZingHR"
)

# Versioning: Mount the v1 router
app.include_router(
    employees.router, 
    prefix="/api/v1/employees", 
    tags=["Employees"]
)

@app.get("/health", tags=["System"])
def health_check():
    """Endpoint for monitoring tools to verify the app is alive."""
    return {"status": "operational", "version": settings.VERSION}





# from fastapi import FastAPI, HTTPException, status
# from pydantic import BaseModel, EmailStr
# from enum import Enum
# import uuid

# app = FastAPI(title="ZingHR Employee Directory API")

# class DepartmentEnum(str, Enum):
#     ENGINEERING = "Engineering"
#     SALES = "Sales"
#     HR = "HR"

# class EmployeeCreate(BaseModel):
#     name: str
#     email: EmailStr
#     department: DepartmentEnum
#     salary: int
    
# class EmployeeResponse(BaseModel):
#     id: str
#     name: str
#     email: EmailStr
#     department: DepartmentEnum
#     salary: int
    
# # In-memory database simulation
# fake_db = {}

# @app.get('/')
# def read_root():
#     return {"status": "healthy", "service": "Employee Directory"}

# @app.post('/employees/', response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
# def create_employee(employee: EmployeeCreate):
#     emp_id = str(uuid.uuid4())
    
#     employee_data = employee.model_dump()
    
#     employee_data['id'] = emp_id
    
#     fake_db[emp_id] = employee_data
#     return employee_data

# @app.get('/employees/{emp_id}', response_model=EmployeeResponse)
# def get_employee(emp_id: str):
#     if emp_id not in fake_db:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Employee with ID {emp_id} not found"
#         )
#     return fake_db[emp_id]

# @app.get('/employees/', response_model=list[EmployeeResponse])
# def list_employees(skip: int = 0, limit: int = 10):
#     db_values = list(fake_db.values())
#     return db_values[skip: skip+ limit]

# @app.put('/employees/{emp_id}', response_model=EmployeeResponse)
# def update_employee(emp_id: str, updated_employee: EmployeeCreate):
#     if emp_id not in fake_db:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Cannot update. Employee with ID {emp_id} not found."
#         )
        
#     update_data = updated_employee.model_dump()
        
#     update_data['id'] = emp_id
        
#     fake_db[emp_id] = update_data
        
#     return update_data
    
# @app.delete('/employees/{emp_id}', status_code=status.HTTP_204_NO_CONTENT)
# def delete_employee(emp_id: str):
#     if emp_id not in fake_db:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Cannot delte. Emplyee wuith ID {emp_id} not found"
#         )
        
#     del fake_db[emp_id]
    
#     return None
        




