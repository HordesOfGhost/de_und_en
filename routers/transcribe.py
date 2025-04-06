from fastapi import APIRouter, Form, Request, File, UploadFile, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from services.db import get_db
from services.transcription import transcribe_and_save  # Define this in services
from .config import templates
import os

router = APIRouter()

# Ensure the `transcribe_and_save` function in services handles saving and processing

@router.get("/transcribe", response_class=HTMLResponse)
async def transcription_form(request: Request):
    return templates.TemplateResponse("transcription.html", {
        "request": request,
        "transcribed_text": "",
        "input_language": "Audio",
        "transcribed_language": "English",  # You can change based on transcription
        "input_audio": ""
    })

@router.post("/transcribe", response_class=HTMLResponse)
async def transcribe(request: Request, audio_file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save the uploaded file temporarily
    audio_path = f"temp_{audio_file.filename}"
    with open(audio_path, "wb") as buffer:
        buffer.write(await audio_file.read())

    # Call transcription service to process the file
    transcribed_text, saved_transcription = transcribe_and_save(audio_path, db)

    # Clean up the saved file
    os.remove(audio_path)

    return templates.TemplateResponse("transcription.html", {
        "request": request,
        "input_language": "Audio",
        "input_audio": audio_file.filename,
        "transcribed_text": transcribed_text,
        "transcribed_language": "English",
    })
