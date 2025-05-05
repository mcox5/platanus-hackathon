# Pydantic Imports
from pydantic import BaseModel
# Libraries Imports
from typing import Optional
# Local Imports

class StudentBase(BaseModel):
    first_names: str
    last_names: str

class StudentCreate(StudentBase):
    pass

class StudentRead(StudentBase):
    id: int

    class Config:
        orm_mode = True

class StudentUpdate(BaseModel):
    first_names: Optional[str] = None
    last_names: Optional[str] = None

    class Config:
        orm_mode = True