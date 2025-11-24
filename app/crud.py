from sqlalchemy.orm import Session

from . import models
from . import schemas

# Get student by ID
def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

# Get paginated list of students
def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()

# Create new student and associate with group
def create_student(db: Session, student: schemas.StudentCreate, group_id: int):
    db_student = models.Student(**student.dict(), group_id=group_id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)  # Refresh to get generated ID and other database values
    return db_student

# Get group by ID
def get_group(db: Session, group_id: int):
    return db.query(models.Group).filter(models.Group.id == group_id).first()

# Get paginated list of groups
def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Group).offset(skip).limit(limit).all()

# Create new group
def create_group(db: Session, group: schemas.GroupCreate):
    db_group = models.Group(**group.dict())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)  # Refresh to get generated ID
    return db_group

# Add existing student to a group
def add_student_to_group(db: Session, student_id: int, group_id: int):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student:
        student.group_id = group_id
        db.commit()
        db.refresh(student)
        return student
    return None  # Return None if student not found

# Remove student from their current group
def remove_student_from_group(db: Session, student_id: int):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student:
        student.group_id = None
        db.commit()
        db.refresh(student)
        return student
    return None  # Return None if student not found