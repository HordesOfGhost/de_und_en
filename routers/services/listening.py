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
from services.listening.listen import generate_listening_content_and_save_metadata
from services.listening.evaluate import evaluate_listening_answers
from services.db import get_db
from sqlalchemy.orm import Session
from typing import List
import json

router = APIRouter()


@router.get("/listening", tags=['listening'], response_class=HTMLResponse, include_in_schema=False)
async def render_listening_page(request: Request):
    """
    Renders the listening practice page.

    Parameters
    -----------
    request : Request
        The incoming HTTP request object for rendering HTML.

    Returns
    --------
    HTMLResponse
        The rendered listening practice page.
    """
    return templates.TemplateResponse("listening.html", {
        "request": request
    })

@router.post("/listening", tags=['listening'], response_class=JSONResponse, include_in_schema=False)
async def get_listening_contents(level: str = Form("A1"), db: Session = Depends(get_db)):
    """
    Generates listening content based on the level and saves metadata.

    Parameters
    -----------
    level : str
        The level of listening practice, e.g., A1, A2, etc.
    db : Session
        The database session.

    Returns
    --------
    JSONResponse
        The generated content, including topic, article, and questions.
    """
    json_data = generate_listening_content_and_save_metadata(level, db)
    return JSONResponse({
        "level": json_data['level'],
        "topic": json_data['topic'],
        "article": json_data['article'],
        "questions_and_answers": json_data['questions_and_answers']
    })

@router.post("/submit-listening-answers", tags=["listening"], response_class=JSONResponse, include_in_schema=False)
async def submit_answers_from_listening(
    user_answers: List[str] = Form(...),
    article: str = Form(...),
    topic: str = Form(...),
    questions_and_answers: List[str] = Form(...),
):
    """
    Submits the user's answers to the listening practice and evaluates them.

    Parameters
    -----------
    user_answers : List[str]
        A list of answers provided by the user.
    article : str
        The article associated with the listening practice.
    topic : str
        The topic of the listening practice.
    questions_and_answers : List[str]
        A list of question-answer pairs for evaluation.

    Returns
    --------
    JSONResponse
        The evaluation results including score, explanation, and correctness.
    """
    
    questions_and_answers = [json.loads(item) for item in questions_and_answers]

    
    explanations_and_scores = evaluate_listening_answers(
        topic=topic,
        article=article,
        questions_and_answers=questions_and_answers,
        user_answers=user_answers
    )

    
    evaluation = [
        {
            "question_number": i + 1,
            "user_answer": user_answers[i],
            "correct_answer": questions_and_answers[i]["answer"],
            "is_correct": explanations_and_scores["score"][i] > 0.5,  
            "explanation": explanations_and_scores["explanation"][i],
        }
        for i in range(len(user_answers))
    ]

    score_str = f"{sum(1 for e in evaluation if e['is_correct'])} / {len(evaluation)}"

    return JSONResponse({
        "evaluation": evaluation,
        "score": score_str,
    })
