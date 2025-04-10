from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.tts import synthesize_text_and_play_audio

router = APIRouter()

@router.post("/synthesize")
async def play_audio_api(text: str, language: str):
    try:
        synthesize_text_and_play_audio(text, language)
        return JSONResponse(status_code=200, content={"message": "Audio played successfully"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
