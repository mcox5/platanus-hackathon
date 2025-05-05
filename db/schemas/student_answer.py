# Pydantic Imports
from pydantic import BaseModel
# Libraries Imports
from typing import Optional
# Local Imports
class StudentAnswerBase(BaseModel):
    content: str
    student_score: int
    model_feedback: str
    positional_index: int
    question_id: int
    test_id: int

class StudentAnswerCreate(StudentAnswerBase):
    pass
class StudentAnswerRead(StudentAnswerBase):
    id: int

    class Config:
        orm_mode = True

class StudentAnswerUpdate(BaseModel):
    content: Optional[str] = None
    student_score: Optional[int] = None
    model_feedback: Optional[str] = None
    positional_index: Optional[int] = None
    question_id: Optional[int] = None
    test_id: Optional[int] = None

    class Config:
        orm_mode = True
