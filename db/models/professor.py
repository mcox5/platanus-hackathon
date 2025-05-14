from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from core.database import Base



class Professor(Base):
    __tablename__ = "professors"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    first_names = Column(String, nullable=False)
    last_names = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())

    guidelines = relationship(
        "db.models.guideline.Guideline",
        back_populates="professor",
        cascade="all, delete-orphan"
    )