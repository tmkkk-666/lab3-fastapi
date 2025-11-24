import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(title="Students API", description="API for managing students and groups")

# Student endpoints
@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, group_id: int, db: Session = Depends(get_db)):
    """Create a new student associated with a group"""
    return crud.create_student(db=db, student=student, group_id=group_id)

@app.get("/students/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    """Get student details by ID"""
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@app.get("/students/", response_model=list[schemas.Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get paginated list of all students"""
    students = crud.get_students(db, skip=skip, limit=limit)
    return students

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """Delete a student by ID"""
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted"}

# Group endpoints
@app.post("/groups/", response_model=schemas.Group)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    """Create a new student group"""
    return crud.create_group(db=db, group=group)

@app.get("/groups/{group_id}", response_model=schemas.Group)
def read_group(group_id: int, db: Session = Depends(get_db)):
    """Get group details by ID"""
    db_group = crud.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group

@app.get("/groups/", response_model=list[schemas.Group])
def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get paginated list of all groups"""
    groups = crud.get_groups(db, skip=skip, limit=limit)
    return groups

@app.delete("/groups/{group_id}")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    """Delete a group by ID"""
    db_group = crud.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    
    db.delete(db_group)
    db.commit()
    return {"message": "Group deleted"}

# Group-student relationship endpoints
@app.post("/groups/{group_id}/students/", response_model=schemas.Student)
def add_student_to_group(student_id: int, group_id: int, db: Session = Depends(get_db)):
    """Add a student to a group"""
    return crud.add_student_to_group(db=db, student_id=student_id, group_id=group_id)

@app.delete("/groups/{group_id}/students/{student_id}")
def remove_student_from_group(group_id: int, student_id: int, db: Session = Depends(get_db)):
    """Remove a student from their current group"""
    return crud.remove_student_from_group(db=db, student_id=student_id)

@app.get("/groups/{group_id}/students/", response_model=list[schemas.Student])
def get_group_students(group_id: int, db: Session = Depends(get_db)):
    """Get all students in a specific group"""
    db_group = crud.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    
    return db_group.students

# Student transfer endpoint
@app.post("/students/{student_id}/transfer")
def transfer_student(student_id: int, new_group_id: int, db: Session = Depends(get_db)):
    """Transfer a student from current group to a new group"""
    student = crud.get_student(db, student_id=student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Remove from current group
    crud.remove_student_from_group(db, student_id)
    
    # Add to new group
    crud.add_student_to_group(db, student_id, new_group_id)
    
    return {"message": f"Student {student_id} transferred to group {new_group_id}"}