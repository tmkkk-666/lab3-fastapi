from pydantic import BaseModel
from typing import List, Optional

# Base schema for student data
class StudentBase(BaseModel):
    name: str    # Student name
    email: str   # Student email

# Schema for student creation
class StudentCreate(StudentBase):
    pass

# Schema for student response
class Student(StudentBase):
    id: int
    group_id: Optional[int] = None
    
    class Config:
        from_attributes = True  # Enable ORM model conversion

# Base schema for group data
class GroupBase(BaseModel):
    name: str  # Group name

# Schema for group creation
class GroupCreate(GroupBase):
    pass

# Schema for group response
class Group(GroupBase):
    id: int
    students: List[Student] = []
    
    class Config:
        from_attributes = True  # Enable ORM model conversion