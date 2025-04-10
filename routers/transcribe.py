from fastapi import APIRouter, Request, File, UploadFile, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from services.db import get_db
from services.transcription import transcribe_audio
from services.translation import translate_and_save
from .config import templates
import os

router = APIRouter()

# Handle POST request for transcription
@router.post("/transcribe", response_class=HTMLResponse)
async def transcribe(
    request: Request,
    audio_file: UploadFile = File(...),
    direction: str = Form(...),
    db: Session = Depends(get_db)
):
    audio_path = f"temp_{audio_file.filename}"
    with open(audio_path, "wb") as buffer:
        buffer.write(await audio_file.read())

    # Map direction to language
    language_code = "en" if direction == "en_to_de" else "de"

    transcribed_text = transcribe_audio(audio_path, db, language=language_code)
    translated_text, saved_translation = translate_and_save(transcribed_text, direction, db)

    os.remove(audio_path)

    return templates.TemplateResponse("transcription.html", {
        "request": request,
        "input_language":"English" if direction == "en_to_de" else "German",
        "input_audio": audio_file.filename,
        "input_text": transcribed_text,
        "translated_language": "German" if direction == "en_to_de" else "English",
        "translated_text":translated_text
    })

@router.get("/transcribe", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("transcription.html", {
        "request": request,
        "transcribed_text": "",
        "input_language": "Audio",
        "transcribed_language": "English",
        "input_audio": ""
    })
