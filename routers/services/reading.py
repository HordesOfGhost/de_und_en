from fastapi import (
    APIRouter, 
    Request, 
    Form, 
    Depends,
    )
from fastapi.responses import (
    HTMLResponse, 
    JSONResponse,
    )
from routers.config import templates
from sqlalchemy.orm import Session
import json
from typing import List
from services.db import get_db
from services.reading.read import generate_reading_content_and_save_metadata
from services.reading.evaluate import evaluate_reading_answers


router = APIRouter()


@router.get("/reading", tags=['reading'], response_class=HTMLResponse, include_in_schema=False)
async def render_reading_page(request: Request):
    """
    Renders the reading page where users can read articles and answer questions.

    Parameters
    -----------
    request : Request
        The incoming HTTP request object for rendering the HTML page.

    Returns
    --------
    HTMLResponse
        The rendered reading page.
    """
    return templates.TemplateResponse("reading.html", {
        "request": request
    })

@router.post("/reading", tags=['reading'], response_class=JSONResponse, include_in_schema=False)
async def get_reading_contents(level: str = Form("A1"), db: Session = Depends(get_db)):
    """
    Generates reading content based on the user's selected level and stores metadata.

    Parameters
    -----------
    level : str
        The proficiency level (e.g., "A1").
    db : Session
        The database session to interact with the database.

    Returns
    --------
    JSONResponse
        The reading content, including the level, topic, article, and questions & answers.
    """
    json_data = generate_reading_content_and_save_metadata(level, db)
    return JSONResponse({
        "level": json_data['level'],
        "topic": json_data['topic'],
        "article": json_data['article'],
        "questions_and_answers": json_data['questions_and_answers']
    })

@router.post("/submit-reading-answers", tags=["reading"], response_class=JSONResponse, include_in_schema=False)
async def submit_answers_from_reading(
    user_answers: List[str] = Form(...),
    article: str = Form(...),
    topic: str = Form(...),
    questions_and_answers: List[str] = Form(...),
):
    """
    Evaluates the user's answers based on the reading article and questions.

    Parameters
    -----------
    user_answers : List[str]
        A list of the user's answers to the questions.
    article : str
        The article the user read.
    topic : str
        The topic of the article.
    questions_and_answers : List[str]
        A list of question-answer pairs.

    Returns
    --------
    JSONResponse
        The evaluation results, including the score and explanations.
    """
    
    questions_and_answers = [json.loads(item) for item in questions_and_answers]


    explanations_and_scores = evaluate_reading_answers(
        topic=topic,
        article=article,
        questions_and_answers=questions_and_answers,
        user_answers=user_answers
    )

    # Prepare evaluation results
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
