from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# Student database model
class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)  # Primary key
    name = Column(String, index=True)  # Student name with index
    email = Column(String, unique=True, index=True)  # Unique student email with index
    
    # Foreign key relationship to Group
    group_id = Column(Integer, ForeignKey("groups.id"))
    # Bidirectional relationship mapping
    group = relationship("Group", back_populates="students")

# Group database model
class Group(Base):
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, index=True)  # Primary key
    name = Column(String, unique=True, index=True)  # Unique group name with index
    
    # Bidirectional relationship mapping
    students = relationship("Student", back_populates="group")