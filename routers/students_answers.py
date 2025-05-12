from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from core.database import get_db
from db.models import StudentAnswer
from db.schemas import StudentAnswerRead, StudentAnswerCreate, StudentAnswerUpdate

router = APIRouter()

@router.post("/students_answers", response_model=StudentAnswerCreate, tags=["students_answers"])
async def add_student_answer(
    student_answer: StudentAnswerCreate,
    db: AsyncSession = Depends(get_db)
):
    new_answer = StudentAnswer(**student_answer.dict())
    db.add(new_answer)
    await db.commit()
    await db.refresh(new_answer)
    return JSONResponse(content={"data": jsonable_encoder(new_answer)})

@router.get("/students_answers/{answer_id}", response_model=StudentAnswerRead, tags=["students_answers"])
async def get_student_answer(
    answer_id: int,
    db: AsyncSession = Depends(get_db)
):
    ans = await db.get(StudentAnswer, answer_id)
    if not ans:
        raise HTTPException(status_code=404, detail="Student answer not found")
    return JSONResponse(content={"data": jsonable_encoder(ans)})

@router.get("/students_answers", response_model=List[StudentAnswerRead], tags=["students_answers"])
async def get_answers_for_test(
    test_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(StudentAnswer).where(StudentAnswer.test_id == test_id))
    return JSONResponse(content={"data": jsonable_encoder(result.scalars().all()), "length": len(result.scalars().all())})

@router.put("/students_answers/{answer_id}", response_model=StudentAnswerRead, tags=["students_answers"])
async def update_student_answer(
    answer_id: int,
    student_answer: StudentAnswerUpdate,
    db: AsyncSession = Depends(get_db)
):
    ans = await db.get(StudentAnswer, answer_id)
    if not ans:
        raise HTTPException(status_code=404, detail="Student answer not found")
    for field, value in student_answer.dict(exclude_unset=True).items():
        setattr(ans, field, value)
    await db.commit()
    await db.refresh(ans)
    return JSONResponse(content={"data": jsonable_encoder(ans)})

@router.delete("/students_answers/{answer_id}", status_code=204, tags=["students_answers"])
async def delete_student_answer(
    answer_id: int,
    db: AsyncSession = Depends(get_db)
):
    ans = await db.get(StudentAnswer, answer_id)
    if not ans:
        raise HTTPException(status_code=404, detail="Student answer not found")
    await db.delete(ans)
    await db.commit()