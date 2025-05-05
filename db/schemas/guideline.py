# Pydantic Imports
from pydantic import BaseModel
# Libraries Imports
from typing import Optional

# Local Imports


class GuidelineBase(BaseModel):
    title: str
    topic: str
    max_score: int
    s3_link: str
    s3_filename: str
    professor_id: int

class GuidelineCreate(GuidelineBase):
    pass

class GuidelineRead(GuidelineBase):
    id: int

    class Config:
        orm_mode = True

class GuidelineUpdate(BaseModel):
    title: Optional[str] = None
    topic: Optional[str] = None
    max_score: Optional[int] = None
    s3_link: Optional[str] = None
    s3_filename: Optional[str] = None
    professor_id: Optional[int] = None

    class Config:
        orm_mode = True
