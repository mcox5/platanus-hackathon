from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from core.database import Base
import enum

class UserType(str, enum.Enum):
    STUDENT = "student"
    PROFESSOR = "professor"

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    
    # Account type (student or professor)
    user_type = Column(Enum(UserType), nullable=False)
    
    # Foreign keys for specific user types
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    professor_id = Column(Integer, ForeignKey("professors.id"), nullable=True)
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships - these will be used to link the account to either a student or professor
    student = relationship("db.models.student.Student", back_populates="account")
    professor = relationship("db.models.professor.Professor", back_populates="account")
