from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from routers.config import templates
from fastapi.templating import Jinja2Templates
from services.reading.read import generate_reading_content_and_save_metadata
from services.reading.evaluate import evaluate_reading_answers
from sqlalchemy.orm import Session
from services.db import get_db

import json
router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/reading", tags=['reading'], response_class=HTMLResponse, include_in_schema=False)
async def get_reading_page(request: Request):
    return templates.TemplateResponse("reading.html", {"request": request})

@router.post("/reading", tags=['reading'], response_class=JSONResponse)
async def get_reading_contents(level: str=Form("A1"), db: Session= Depends(get_db)):
    json_data = generate_reading_content_and_save_metadata(level, db)
    return JSONResponse({
        "level":json_data['level'],
        "topic":json_data['topic'],
        "article":json_data['article'],
        "questions_and_answers":json_data['questions_and_answers']
    })

from fastapi import Form
from typing import List
@router.post("/submit-reading-answers", tags=["reading"], response_class=JSONResponse)
async def submit_answers_from_reading(
    user_answers: List[str] = Form(...),
    article: str = Form(...),
    topic: str = Form(...),
    questions_and_answers: List[str] = Form(...)
):
    # Parse list of question-answer JSON strings
    questions_and_answers = [json.loads(item) for item in questions_and_answers]

    # Evaluate answers
    explanations_and_scores = evaluate_reading_answers(
        topic=topic,
        article=article,
        questions_and_answers=questions_and_answers,
        user_answers=user_answers
    )

    # Compose response per question
    evaluation = [
        {
            "question_number": i + 1,
            "user_answer": user_answers[i],
            "correct_answer": questions_and_answers[i]["answer"],
            "is_correct": explanations_and_scores["score"][i] > 0.5,  # Threshold (you can adjust this)
            "explanation": explanations_and_scores["explanation"][i],
        }
        for i in range(len(user_answers))
    ]

    score_str = f"{sum(1 for e in evaluation if e['is_correct'])} / {len(evaluation)}"

    return JSONResponse({
        "evaluation": evaluation,
        "score": score_str,
    })
