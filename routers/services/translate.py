from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from services.db import get_db
from services.translation import translate_translation_and_save
from routers.config import templates

router = APIRouter()

@router.get("/translate",tags=['translate'], response_class=HTMLResponse)
async def translation_page(request: Request, direction: str = "en_to_de"):
    return templates.TemplateResponse("translation.html", {
        "request": request,
        "direction": direction,
        "translated_text": "",
        "input_language": "English" if direction == "en_to_de" else "German",
        "translated_language": "German" if direction == "en_to_de" else "English",
        "input_text": ""
    })

@router.post("/translate",tags=['translate'], response_class=HTMLResponse)
async def translate(request: Request, input_text: str = Form(...), direction: str = Form(...), db: Session = Depends(get_db)):
    translated_text, saved_translation = translate_translation_and_save(input_text, direction, db)

    return templates.TemplateResponse("translation.html", {
        "request": request,
        "input_language":"English" if direction == "en_to_de" else "German",
        "input_text":input_text,
        "translated_text": translated_text,
        "translated_language": "German" if direction == "en_to_de" else "English",
        "direction": direction
    })