from pydantic import BaseModel
from typing import Optional, List, Dict

# --- Professor Schemas ---
class ProfessorBase(BaseModel):
    email: str

class ProfessorCreate(ProfessorBase):
    pass

class ProfessorRead(ProfessorBase):
    id: int

    class Config:
        orm_mode = True

class ProfessorUpdate(BaseModel):
    email: Optional[str] = None

    class Config:
        orm_mode = True