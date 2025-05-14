# Libraries Imports
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_names = Column(String, nullable=False)
    last_names = Column(String, nullable=False)

    # Account relationship
    account = relationship(
        "db.models.account.Account",
        back_populates="student",
        uselist=False
    )
    
    tests = relationship(
        "db.models.test.Test",
        back_populates="student",
        cascade="all, delete-orphan"
    )
    students_answers = relationship(
        "db.models.student_answer.StudentAnswer",
        back_populates="student",
        cascade="all, delete-orphan"
    )