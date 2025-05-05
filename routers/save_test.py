from fastapi import APIRouter, Form, UploadFile, File, Depends
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from db.models import Question, Test, StudentAnswer
from services.s3 import upload_test
from services.processing import proses_file_function, parse_ocr_function

router = APIRouter()

@router.post("/saveTest/", tags=["tests"])
async def save_test(
    guideline_id: int = Form(...),
    files: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db),
):
    files_meta = await upload_test(files)
    result = await db.execute(select(Question).where(Question.guideline_id == guideline_id))
    questions = {q.positional_index: q for q in result.scalars().all()}
    created = []
    for f in files_meta['files']:
        test = Test(guideline_id=guideline_id, title=f['filename'], s3_link=f['url'], s3_filename=f['filename'], student_id=1)
        db.add(test)
        await db.flush()
        data = parse_ocr_function((await proses_file_function(f"data/{f['filename']}"))["result"])
        answers = []
        for idx_str, qa in data.items():
            idx = int(idx_str)
            q = questions.get(idx)
            if not q: continue
            answers.append(StudentAnswer(test_id=test.id, question_id=q.id, positional_index=idx, content=qa['answer']))
        db.add_all(answers)
        await db.commit()
        created.append({"test": test, "answers": answers})
    return {"message": "Files saved", "data": created}