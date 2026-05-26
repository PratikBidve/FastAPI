from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.api.dependencies import get_db
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.db import models

router = APIRouter()


# ---------------------------------------------------------------------------
# POST /  — Create
# ---------------------------------------------------------------------------
@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Employee).filter(models.Employee.email == employee.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_emp = models.Employee(id=str(uuid.uuid4()), **employee.model_dump())
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return new_emp


# ---------------------------------------------------------------------------
# GET /  — List with pagination
# ---------------------------------------------------------------------------
@router.get("/", response_model=List[EmployeeResponse])
def list_employees(
    skip: int = Query(default=0, ge=0, description="Records to skip"),
    limit: int = Query(default=10, ge=1, le=100, description="Max records to return"),
    db: Session = Depends(get_db),
):
    """Paginated employee list. Use skip/limit for cursor-style pagination."""
    employees = db.query(models.Employee).offset(skip).limit(limit).all()
    return employees


# ---------------------------------------------------------------------------
# GET /{emp_id}  — Read single
# ---------------------------------------------------------------------------
@router.get("/{emp_id}", response_model=EmployeeResponse)
def read_employee(emp_id: str, db: Session = Depends(get_db)):
    db_emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_emp


# ---------------------------------------------------------------------------
# PUT /{emp_id}  — Update (partial fields supported)
# ---------------------------------------------------------------------------
@router.put("/{emp_id}", response_model=EmployeeResponse)
def update_employee(emp_id: str, payload: EmployeeUpdate, db: Session = Depends(get_db)):
    """Update one or more fields. Only provided (non-None) fields are changed."""
    db_emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    if not db_emp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {emp_id} not found",
        )

    # If updating email, enforce uniqueness against other records
    if payload.email and payload.email != db_emp.email:
        conflict = (
            db.query(models.Employee)
            .filter(models.Employee.email == payload.email)
            .first()
        )
        if conflict:
            raise HTTPException(status_code=400, detail="Email already in use by another employee")

    # Apply only the fields that were explicitly set in the request body
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_emp, field, value)

    db.commit()
    db.refresh(db_emp)
    return db_emp


# ---------------------------------------------------------------------------
# DELETE /{emp_id}  — Delete
# ---------------------------------------------------------------------------
@router.delete("/{emp_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(emp_id: str, db: Session = Depends(get_db)):
    db_emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    if not db_emp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {emp_id} not found",
        )
    db.delete(db_emp)
    db.commit()
    return None
