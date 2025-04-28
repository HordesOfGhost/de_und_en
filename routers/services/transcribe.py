from fastapi import APIRouter, Request, File, UploadFile, Depends, Form
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from services.db import get_db
from services.transcription import transcribe_audio
from services.translation import translate_translation_and_save_with_gemini
from routers.config import templates

router = APIRouter()

@router.get("/transcribe",tags=['transcribe'], response_class=HTMLResponse, include_in_schema=False)
async def transcribe_page(request: Request):
    return templates.TemplateResponse("transcription.html", {
        "request": request,
        "transcribed_text": "",
        "input_language": "Audio",
        "transcribed_language": "English",
        "input_audio": ""
    })

@router.post("/transcribe", tags=['transcribe'])
async def transcribe(
    request: Request,
    audio_file: UploadFile = File(...),
    direction: str = Form("en_to_de"),
    db: Session = Depends(get_db)
):
    audio_bytes =await audio_file.read()

    # Map direction to language
    language_code = "en" if direction == "en_to_de" else "de"

    # Transcribe and translate
    transcribed_text = transcribe_audio(audio_bytes, language=language_code)
    translated_text, record_id = translate_translation_and_save_with_gemini(transcribed_text, direction, db)

    return JSONResponse({
        "id":record_id,
        "input_language": "English" if direction == "en_to_de" else "German",
        "input_audio": audio_file.filename,
        "input_text": transcribed_text,
        "translated_language": "German" if direction == "en_to_de" else "English",
        "translated_text": translated_text
    })
