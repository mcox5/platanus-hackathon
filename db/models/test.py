# Libraries Imports
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

# Local Imports


class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    student_score = Column(Integer, nullable=False)
    s3_link = Column(String, nullable=False)
    s3_filename = Column(String, nullable=False)
    positional_index = Column(Integer, nullable=False)
    guideline_id = Column(Integer, ForeignKey("guidelines.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)

    guideline = relationship("db.models.guideline.Guideline", back_populates="tests")
    student = relationship("db.models.student.Student", back_populates="tests")
    students_answers = relationship("db.models.student_answer.StudentAnswer", back_populates="test")