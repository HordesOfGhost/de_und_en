from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from routers.config import templates
from fastapi.templating import Jinja2Templates
# from services.writing.read import generate_writing_content_and_save_metadata
# from services.writing.evaluate import evaluate_writing_answers
from sqlalchemy.orm import Session
from services.db import get_db
from services.writing.write import generate_writing_topic
from services.writing.evaluate import evaluate_writing_answers
router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/writing", tags=['writing'], response_class=HTMLResponse, include_in_schema=False)
async def get_writing_page(request: Request):
    return templates.TemplateResponse("writing.html", {"request": request})

@router.post("/writing-topic", tags=["writing"])
async def get_writing_topic(level: str = Form(...), db:Session = Depends(get_db)):
    try:
        print("here")
        selected_topic = generate_writing_topic(level, db)
        return selected_topic
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@router.post("/submit-writing", tags=["writing"], response_class=JSONResponse)
async def submit_evaluate_and_save_writing(
    level: str = Form(...),
    topic: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    # Evaluate the user response (text)
    score_and_explanations_json = evaluate_writing_answers(topic=topic, content=content, level=level, db=db)

    return JSONResponse({
        "level": level,
        "topic": topic,
        "score": score_and_explanations_json.get("score"),
        "evaluation": score_and_explanations_json.get("evaluation")
    })
