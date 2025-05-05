from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from core.database import get_db
from db.models import Student
from db.schemas import StudentRead, StudentBase, StudentCreate, StudentUpdate

router = APIRouter()

@router.get("/students", response_model=List[StudentRead], tags=["students"])
async def get_students(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student))
    return JSONResponse(content={"data": jsonable_encoder(result.scalars().all()), "length": len(result.scalars().all())})

@router.get("/students/{student_id}", response_model=StudentRead, tags=["students"])
async def get_student(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):
    obj = await db.get(Student, student_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Student not found")
    return JSONResponse(content={"data": obj})

@router.post("/students", response_model=StudentRead, tags=["students"])
async def add_student(
    student: StudentCreate,
    db: AsyncSession = Depends(get_db)
):
    new_student = Student(**student.dict())
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    return JSONResponse(content={"data": new_student})

@router.put("/students/{student_id}", response_model=StudentRead, tags=["students"])
async def update_student(
    student_id: int,
    student: StudentUpdate,
    db: AsyncSession = Depends(get_db)
):
    obj = await db.get(Student, student_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Student not found")
    for field, value in student.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    await db.commit()
    await db.refresh(obj)
    return JSONResponse(content={"data": obj})

@router.delete("/students/{student_id}", status_code=204, tags=["students"])
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):
    obj = await db.get(Student, student_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Student not found")
    await db.delete(obj)
    await db.commit()