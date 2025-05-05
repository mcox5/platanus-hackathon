from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from core.database import get_db
from db.models import Question
from db.schemas import QuestionRead, QuestionBase, QuestionCreate, QuestionUpdate

router = APIRouter()

@router.get("/questions/{guideline_id}", response_model=List[QuestionRead], tags=["questions"])
async def get_guideline_questions(
    guideline_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Question).where(Question.guideline_id == guideline_id))
    return JSONResponse(content={"data": jsonable_encoder(result.scalars().all()), "length": len(result.scalars().all())})
