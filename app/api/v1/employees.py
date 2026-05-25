from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas.employee import EmployeeCreate, EmployeeResponse
from app.db import models
import uuid

router = APIRouter()

@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    # 1. Check if email already exists (Enterprise data integrity)
    existing_user = db.query(models.Employee).filter(models.Employee.email == employee.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Map Pydantic to SQLAlchemy Model
    new_emp = models.Employee(
        id=str(uuid.uuid4()),
        **employee.model_dump()
    )
    
    # 3. Transaction Management: Atomic operations
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp) # Get the newly generated ID back from DB
    return new_emp

@router.get("/{emp_id}", response_model=EmployeeResponse)
def read_employee(emp_id: str, db: Session = Depends(get_db)):
    db_emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_emp


@router.delete("/{emp_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(emp_id: str, db: Session = Depends(get_db)):
    # 1. Fetch the record from the DB
    db_emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    
    # 2. If it doesn't exist, 404 is the standard response
    if not db_emp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {emp_id} not found"
        )
    
    # 3. Perform the deletion
    db.delete(db_emp)
    db.commit()
    
    # 4. Return None (204 No Content needs an empty body)
    return None