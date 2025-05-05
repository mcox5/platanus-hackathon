
# Libraries Imports
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    question_type = Column(String, nullable=False)
    max_score = Column(Integer, nullable=False)
    guideline_answer = Column(String, nullable=False)
    positional_index = Column(Integer, nullable=False)
    guideline_id = Column(Integer, ForeignKey("guidelines.id"), nullable=False)

    guideline = relationship("db.models.guideline.Guideline", back_populates="questions")
    students_answers = relationship(
        "db.models.student_answer.StudentAnswer",
        back_populates="question",
        cascade="all, delete-orphan"
    )