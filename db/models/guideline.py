from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class Guideline(Base):
    __tablename__ = "guidelines"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    max_score = Column(Integer, nullable=False)
    s3_link = Column(String, nullable=False)
    s3_filename = Column(String, nullable=False)
    professor_id = Column(Integer, ForeignKey("professors.id"), nullable=False)

    professor = relationship("db.models.professor.Professor", back_populates="guidelines")
    questions = relationship("db.models.question.Question", back_populates="guideline")
    tests = relationship("db.models.test.Test", back_populates="guideline")