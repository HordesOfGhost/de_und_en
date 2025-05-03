from fastapi import (
    APIRouter, 
    Request, 
    Depends,
    Form, 
    )
from fastapi.responses import ( 
    JSONResponse, 
    HTMLResponse,
    )
from sqlalchemy.orm import Session
from services.db import get_db
from services.translation import translate_translation_and_save_with_gemini
from routers.config import templates

router = APIRouter()

@router.get("/translate", tags=['translate'], response_class=HTMLResponse, include_in_schema=False)
async def render_translation_page(request: Request, direction: str = "en_to_de"):
    """
    Serve the translation page.
    Parameters
    -----------
    request: Request
        The request object containing the incoming request.
    direction: str
        The direction for translation, defaulting to "en_to_de" (English to German).
    """
    return templates.TemplateResponse("translation.html", {
        "request": request,
        "direction": direction
    })

@router.post("/translate", tags=['translate'])
async def translate(input_text: str = Form(...), direction: str = Form("en_to_de"), db: Session = Depends(get_db)):
    """
    Translate the input text from one language to another and save the translation.
    Parameters
    -----------
    input_text: str
        The text to be translated.
    direction: str
        The translation direction (default is "en_to_de").
    db: Session
        The database session to store the translation.
    
    Returns
    --------
    JSONResponse
        The response containing the original and translated text, along with metadata.
    """
    try:
        translated_text, record_id = translate_translation_and_save_with_gemini(input_text, direction, db)

        # Return the translated result
        return JSONResponse({
            "id": record_id,
            "input_text": input_text,
            "translated_text": translated_text,
            "input_language": "English" if direction == "en_to_de" else "German",
            "translated_language": "German" if direction == "en_to_de" else "English",
            "direction": direction
        })

    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={"error": "An error occurred during translation."}
        )
