from fastapi import APIRouter, UploadFile, File, HTTPException
from services.s3 import upload_pauta

router = APIRouter()

@router.post("/pauta/", tags=["files"])
async def upload_pauta_file(file: UploadFile = File(...)):
    return await upload_pauta(file)