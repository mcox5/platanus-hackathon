from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

# --- Professor Schemas ---
class ProfessorBase(BaseModel):
    email: str
    first_names: str
    last_names: str

class ProfessorCreate(ProfessorBase):
    pass

class ProfessorRead(ProfessorBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ProfessorUpdate(BaseModel):
    email: Optional[str] = None
    first_names: Optional[str] = None
    last_names: Optional[str] = None

    class Config:
        orm_mode = True