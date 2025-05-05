# Pydantic Imports
from pydantic import BaseModel
# Libraries Imports
from typing import Optional
# Local Imports

class TestBase(BaseModel):
    title: str
    student_score: int
    s3_link: str
    s3_filename: str
    positional_index: int
    guideline_id: int
    student_id: int

class TestCreate(TestBase):
    pass

class TestRead(TestBase):
    id: int

    class Config:
        orm_mode = True

class TestUpdate(BaseModel):
    title: Optional[str] = None
    student_score: Optional[int] = None
    s3_link: Optional[str] = None
    s3_filename: Optional[str] = None
    positional_index: Optional[int] = None
    guideline_id: Optional[int] = None
    student_id: Optional[int] = None

    class Config:
        orm_mode = True
