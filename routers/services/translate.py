from fastapi.responses import JSONResponse, HTMLResponse
from fastapi import APIRouter, Form, Request, Depends
from sqlalchemy.orm import Session
from services.db import get_db
from services.translation import translate_translation_and_save_with_gemini
from routers.config import templates

router = APIRouter()


@router.get("/translate", tags=['translate'], response_class=HTMLResponse, include_in_schema=False)
async def translation_page(request: Request, direction: str = "en_to_de"):
    return templates.TemplateResponse("translation.html", {
        "request": request,
        "direction": direction
    })

@router.post("/translate", tags=['translate'])
async def translate(input_text: str = Form(...), direction: str = Form("en_to_de"), db: Session = Depends(get_db)):
    translated_text, record_id = translate_translation_and_save_with_gemini(input_text, direction, db)
    return JSONResponse({
        "id": record_id,
        "input_text": input_text,
        "translated_text": translated_text,
        "input_language": "English" if direction == "en_to_de" else "German",
        "translated_language": "German" if direction == "en_to_de" else "English",
        "direction": direction
    })
