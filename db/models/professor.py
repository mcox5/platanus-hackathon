from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base



class Professor(Base):
    __tablename__ = "professors"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)

    guidelines = relationship(
        "db.models.guideline.Guideline",
        back_populates="professor",
        cascade="all, delete-orphan"
    )