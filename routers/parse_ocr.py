from fastapi import APIRouter, HTTPException
from typing import List
from services.processing import parse_ocr_function

router = APIRouter()

@router.post("/parseOcr/", tags=["processing"])
async def parse_ocr_answer(ocr_answer: List[str]):
    try:
        return parse_ocr_function(ocr_answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))