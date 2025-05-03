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
from services.db import get_db
from services.writing.write import generate_writing_topic
from services.writing.evaluate import evaluate_writing_answers

router = APIRouter()

@router.get("/writing", tags=['writing'], response_class=HTMLResponse, include_in_schema=False)
async def render_writing_page(request: Request):
    """
    Serve the writing page.

    Parameters:
    -----------
    request: Request
        The request object containing the incoming request.
    
    Returns:
    --------
    HTMLResponse
        The rendered HTML template for the writing page.
    """
    return templates.TemplateResponse("writing.html", {"request": request})

@router.post("/writing-topic", tags=["writing"])
async def get_writing_topic(level: str = Form(...), db: Session = Depends(get_db), include_in_schema=False):
    """
    Generate a writing topic based on the selected level.

    Parameters:
    -----------
    level: str
        The selected level for the writing topic (e.g., A1, B1, C1).
    db: Session
        The database session injected via dependency.

    Returns:
    --------
    JSONResponse
        A JSON response containing the generated writing topic or an error message.
    """
    try:
        selected_topic = generate_writing_topic(level, db)
        return selected_topic
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Failed to generate writing topic."} 
        )

@router.post("/submit-writing", tags=["writing"], response_class=JSONResponse, include_in_schema=False)
async def submit_evaluate_and_save_writing(
    level: str = Form(...),
    topic: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Submit the writing content, evaluate it, and save the result.

    Parameters:
    -----------
    level: str
        The selected writing level (e.g., A1, B1, C1).
    topic: str
        The writing topic selected by the user.
    content: str
        The writing content submitted by the user.
    db: Session
        The database session injected via dependency.

    Returns:
    --------
    JSONResponse
        A JSON response containing the evaluation score, explanation, and other details.
    """
    try:
        score_and_explanations_json = evaluate_writing_answers(topic=topic, content=content, level=level, db=db)

        return JSONResponse({
            "level": level,
            "topic": topic,
            "score": score_and_explanations_json.get("score"),
            "evaluation": score_and_explanations_json.get("evaluation")
        })
    
    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={"error": "An error occurred while evaluating your writing."}
        )