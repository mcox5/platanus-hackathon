import uuid
from typing import List
from fastapi import UploadFile
from services.aws import AWS_S3_CLIENT, S3_BUCKET


async def upload_pauta(file: UploadFile) -> dict:
    """
    Uploads a single file to S3 under a 'pauta/' prefix.
    Returns a dict with the original filename and the public URL.
    """
    contents = await file.read()
    key = f"pauta/{uuid.uuid4()}_{file.filename}"
    AWS_S3_CLIENT.put_object(Bucket=S3_BUCKET, Key=key, Body=contents)
    url = f"https://{S3_BUCKET}.s3.amazonaws.com/{key}"
    return {"filename": file.filename, "url": url}


async def upload_test(files: List[UploadFile]) -> dict:
    """
    Uploads multiple files to S3 under a 'test/' prefix.
    Returns a dict with a list of file metadata (filename and URL).
    """
    uploaded = []
    for file in files:
        contents = await file.read()
        key = f"test/{uuid.uuid4()}_{file.filename}"
        AWS_S3_CLIENT.put_object(Bucket=S3_BUCKET, Key=key, Body=contents)
        url = f"https://{S3_BUCKET}.s3.amazonaws.com/{key}"
        uploaded.append({"filename": file.filename, "url": url})
    return {"files": uploaded}
