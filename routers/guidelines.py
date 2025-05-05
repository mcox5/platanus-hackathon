from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from core.database import get_db
from db.models import Guideline
from db.schemas import GuidelineRead, GuidelineCreate, GuidelineUpdate

import json

def guidelines_to_json(guidelines: List[Guideline]):
    return json.dumps([guideline.to_dict() for guideline in guidelines])

router = APIRouter()

@router.get("/guidelines", response_model=List[GuidelineRead], tags=["guidelines"])
async def get_guidelines(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Guideline))
    guidelines = result.scalars().all()
    if not guidelines:
        raise HTTPException(status_code=404, detail="No guidelines found")
    return JSONResponse(content={"data": jsonable_encoder(guidelines), "length": len(guidelines)})

@router.post("/guidelines/", response_model=GuidelineRead, tags=["guidelines"])
async def add_guideline(
    guideline: GuidelineCreate,
    db: AsyncSession = Depends(get_db)
):
    new_guideline = Guideline(**guideline.dict())
    db.add(new_guideline)
    await db.commit()
    await db.refresh(new_guideline)
    return JSONResponse(content={"data": new_guideline})

@router.put("/guidelines/{guideline_id}", response_model=GuidelineRead, tags=["guidelines"])
async def update_guideline(
    guideline_id: int,
    guideline: GuidelineUpdate,
    db: AsyncSession = Depends(get_db)
):
    obj = await db.get(Guideline, guideline_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Guideline not found")
    for field, value in guideline.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    await db.commit()
    await db.refresh(obj)
    return JSONResponse(content={"data": obj})

@router.delete("/guidelines/{guideline_id}", status_code=204, tags=["guidelines"])
async def delete_guideline(
    guideline_id: int,
    db: AsyncSession = Depends(get_db)
):
    obj = await db.get(Guideline, guideline_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Guideline not found")
    await db.delete(obj)
    await db.commit()