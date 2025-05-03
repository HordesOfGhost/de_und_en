from fastapi import (
    APIRouter, 
    Request, 
    UploadFile, 
    Depends, 
    Form,
    File, 
    )
from fastapi.responses import (
    HTMLResponse, 
    JSONResponse,
    )
from sqlalchemy.orm import Session
from routers.config import templates
from services.db import get_db
from services.transcription import transcribe_audio
from services.translation import translate_translation_and_save_with_gemini

router = APIRouter()

@router.get("/transcribe", tags=['transcribe'], response_class=HTMLResponse, include_in_schema=False)
async def render_transcribe_page(request: Request):
    """
    Serve the page for audio transcription and translation.
    """
    return templates.TemplateResponse("transcription.html", {
        "request": request,
        "transcribed_text": "",
        "input_language": "Audio",
        "transcribed_language": "English",
        "input_audio": ""
    })

@router.post("/transcribe", tags=['transcribe'])
async def transcribe(
    audio_file: UploadFile = File(...),
    direction: str = Form("en_to_de"),
    db: Session = Depends(get_db)
):
    """
    Transcribe and translate the given audio file.

    Parameters
    -----------
    audio_file : UploadFile
        The audio file uploaded for transcription.
    direction : str
        The translation direction (e.g., "en_to_de").
    db : Session
        The database session for saving the translation.

    Returns
    --------
    JSONResponse
        The response containing transcribed and translated text along with metadata.
    """
    try:
        audio_bytes = await audio_file.read()

        language_code = "en" if direction == "en_to_de" else "de"

        transcribed_text = transcribe_audio(audio_bytes, language=language_code)

        translated_text, record_id = translate_translation_and_save_with_gemini(transcribed_text, direction, db)

        return JSONResponse({
            "id": record_id,
            "input_language": "English" if direction == "en_to_de" else "German",
            "input_audio": audio_file.filename,
            "input_text": transcribed_text,
            "translated_language": "German" if direction == "en_to_de" else "English",
            "translated_text": translated_text
        })

    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={"error": "An error occurred during transcription or translation."}
        )
