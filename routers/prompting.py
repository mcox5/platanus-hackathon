from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, List
from core.database import get_db
from db.models import Question, StudentAnswer
from services.bedrock import correct_exam

router = APIRouter()

@router.get("/get_prompting_data", tags=["prompting"])
async def get_prompting_data(
    guideline_id: int,
    test_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Question).where(Question.guideline_id == guideline_id))
    questions = result.scalars().all()
    print("questions", questions)
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found")

    guideline_info: Dict[int, Dict] = {}
    answer_info: Dict[int, Dict] = {}
    parsed: List[Dict] = []

    for idx, q in enumerate(questions):
        ans_res = await db.execute(
            select(StudentAnswer.content, StudentAnswer.id).where(
                StudentAnswer.question_id == q.id,
                StudentAnswer.test_id == test_id
            )
        )
        row = ans_res.one_or_none()
        if row:
            answer_id, content = row.id, row.content or ""
        else:
            answer_id, content = None, ""
        print("answer_id", answer_id)
        print("content", content)
        guideline_info[idx] = {"question": q.title, "answer": q.guideline_answer}
        answer_info[idx] = {"answer": content}
        parsed.append({
            "studentAnswerId": answer_id,
            "questionNumber": q.id,
            "question_type": "development",
            "question": q.title,
            "guidelineAnswer": q.guideline_answer,
            "studentAnswer": content,
            "studentScore": 0,
            "modelFeedback": False,
        })

    scores = await correct_exam(guideline_info, answer_info)
    if not isinstance(scores, str):
        result_list: List[Dict] = []
        for idx, item in enumerate(parsed):
            item["studentScore"] = scores[str(idx)]["score"]
            item["modelFeedback"] = scores[str(idx)]["feedback"]
            result_list.append(item)
        return JSONResponse(content={"data": jsonable_encoder(result_list)})
    return JSONResponse(content={"data": jsonable_encoder(parsed)})