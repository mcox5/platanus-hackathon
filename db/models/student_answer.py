# Libraries Imports
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

# Local Imports

class StudentAnswer(Base):
    __tablename__ = "students_answers"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    student_score = Column(Integer, nullable=False)
    model_feedback = Column(String, nullable=False)
    positional_index = Column(Integer, nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)

    question = relationship("db.models.question.Question", back_populates="students_answers")
    test = relationship("db.models.test.Test", back_populates="students_answers")
    student = relationship("db.models.student.Student", back_populates="students_answers")