# Pydantic Imports
from pydantic import BaseModel
# Libraries Imports
from typing import Optional
# Local Imports

class QuestionBase(BaseModel):
    title: str
    question_type: str
    max_score: int
    guideline_answer: str
    positional_index: int
    guideline_id: int

class QuestionCreate(QuestionBase):
    pass

class QuestionRead(QuestionBase):
    id: int

    class Config:
        orm_mode = True

class QuestionUpdate(BaseModel):
    title: Optional[str] = None
    question_type: Optional[str] = None
    max_score: Optional[int] = None
    guideline_answer: Optional[str] = None
    positional_index: Optional[int] = None
    guideline_id: Optional[int] = None

    class Config:
        orm_mode = True