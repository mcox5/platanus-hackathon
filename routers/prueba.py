from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from services.s3 import upload_test

router = APIRouter()

@router.post("/prueba/", tags=["files"])
async def upload_prueba_files(files: List[UploadFile] = File(...)):
    return await upload_test(files)