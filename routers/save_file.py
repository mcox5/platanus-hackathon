from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from db.models import Guideline, Question
from services.s3 import upload_pauta
from services.processing import proses_file_function, parse_ocr_function

router = APIRouter()

@router.post("/saveFile/", tags=["guidelines"])
async def save_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    file_in_s3 = await upload_pauta(file)
    new_guideline = Guideline(
        title=file_in_s3['filename'],
        s3_link=file_in_s3['url'],
        s3_filename=file_in_s3['filename'],
        professor_id=1  # set as needed
    )
    db.add(new_guideline)
    await db.flush()
    questions_data = parse_ocr_function((await proses_file_function(f"data/{file_in_s3['filename']}"))["result"])
    questions = [
        Question(
            guideline_id=new_guideline.id,
            positional_index=idx,
            title=q['question'],
            guideline_answer=q['answer'],
            max_score=10,
        ) for idx, q in questions_data.items()
    ]
    db.add_all(questions)
    await db.commit()
    await db.refresh(new_guideline)
    return {"message": "File saved successfully", "guideline": new_guideline}