from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from core.database import get_db
from db.models import Test
from db.schemas import TestRead, TestBase, TestCreate, TestUpdate

router = APIRouter()

@router.post("/tests", response_model=TestRead, tags=["tests"])
async def add_test(
    test: TestCreate,
    db: AsyncSession = Depends(get_db)
):
    new_test = Test(**test.dict())
    db.add(new_test)
    await db.commit()
    await db.refresh(new_test)
    return JSONResponse(content={"data": new_test})

@router.get("/tests/{test_id}", response_model=TestRead, tags=["tests"])
async def get_test(
    test_id: int,
    db: AsyncSession = Depends(get_db)
):
    obj = await db.get(Test, test_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Test not found")
    return JSONResponse(content={"data": obj})

@router.put("/tests/{test_id}", response_model=TestRead, tags=["tests"])
async def update_test(
    test_id: int,
    test: TestUpdate,
    db: AsyncSession = Depends(get_db)
):
    obj = await db.get(Test, test_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Test not found")
    for field, value in test.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    await db.commit()
    await db.refresh(obj)
    return JSONResponse(content={"data": obj})

@router.get("/tests", response_model=List[TestRead], tags=["tests"])
async def get_tests(
    guideline_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Test).where(Test.guideline_id == guideline_id))
    return JSONResponse(content={"data": jsonable_encoder(result.scalars().all()), "length": len(result.scalars().all())})

@router.delete("/tests/{test_id}", status_code=204, tags=["tests"])
async def delete_test(
    test_id: int,
    db: AsyncSession = Depends(get_db)
):
    obj = await db.get(Test, test_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Test not found")
    await db.delete(obj)
    await db.commit()