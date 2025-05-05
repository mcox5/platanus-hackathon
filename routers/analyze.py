from fastapi import APIRouter, HTTPException
from typing import List
from services.processing import proses_file_function

router = APIRouter()

@router.post("/analyze/", tags=["processing"])
async def analyze_file_s3(file_key: str):
    try:
        result = await proses_file_function(file_key)
        if result.get("job_status") == 'FAILED':
            raise HTTPException(status_code=500, detail="Textract analysis failed.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))