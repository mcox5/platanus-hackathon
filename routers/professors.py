from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import List, Optional
from core.database import get_db
from db.models import Professor
from db.schemas import ProfessorCreate, ProfessorRead, ProfessorUpdate

router = APIRouter()

@router.post("/professors", response_model=ProfessorRead, tags=["professors"])
async def create_professor(
    professor: ProfessorCreate,
    db: AsyncSession = Depends(get_db)
):
    new_professor = Professor(**professor.dict())
    db.add(new_professor)
    await db.commit()
    await db.refresh(new_professor)
    return JSONResponse(content={"data": jsonable_encoder(new_professor)})

@router.get("/professors/{professor_id}", response_model=ProfessorRead, tags=["professors"])
async def get_professor(
    professor_id: int,
    db: AsyncSession = Depends(get_db)
):
    professor = await db.get(Professor, professor_id)
    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")
    return JSONResponse(content={"data": jsonable_encoder(professor)})

@router.get("/professors", response_model=List[ProfessorRead], tags=["professors"])
async def get_all_professors(
    search: Optional[str] = Query(None, description="Search by name or email"),
    db: AsyncSession = Depends(get_db)
):
    query = select(Professor)
    
    # Add search filter if provided
    if search:
        query = query.filter(
            or_(
                Professor.first_names.ilike(f"%{search}%"),
                Professor.last_names.ilike(f"%{search}%"),
                Professor.email.ilike(f"%{search}%")
            )
        )
        
    result = await db.execute(query)
    professors = result.scalars().all()
    return JSONResponse(content={"data": jsonable_encoder(professors), "length": len(professors)})

@router.put("/professors/{professor_id}", response_model=ProfessorRead, tags=["professors"])
async def update_professor(
    professor_id: int,
    professor_data: ProfessorUpdate,
    db: AsyncSession = Depends(get_db)
):
    professor = await db.get(Professor, professor_id)
    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")
    
    # Update only the fields that were provided
    for field, value in professor_data.dict(exclude_unset=True).items():
        setattr(professor, field, value)
    
    await db.commit()
    await db.refresh(professor)
    return JSONResponse(content={"data": jsonable_encoder(professor)})

@router.delete("/professors/{professor_id}", status_code=204, tags=["professors"])
async def delete_professor(
    professor_id: int,
    db: AsyncSession = Depends(get_db)
):
    professor = await db.get(Professor, professor_id)
    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")
    
    await db.delete(professor)
    await db.commit()
    return JSONResponse(content={"message": "Professor deleted successfully"})
