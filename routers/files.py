from fastapi import APIRouter, HTTPException
from services.aws import AWS_S3_CLIENT, S3_BUCKET

router = APIRouter()

@router.get("/list_files/", tags=["files"])
async def list_files():
    try:
        files = AWS_S3_CLIENT.list_objects(Bucket=S3_BUCKET)
        return [f['Key'] for f in files.get('Contents', [])]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))