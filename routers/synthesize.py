from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse, Response
from services.tts import synthesize_text_and_play_audio

router = APIRouter()

@router.get("/synthesize")
async def play_audio_api(text: str = Query(...), language: str = Query(...)):
    try:
        wav_bytes = synthesize_text_and_play_audio(text, language)
        return Response(content=wav_bytes, media_type="audio/wav")

        return JSONResponse(status_code=200, content={"message": "Audio played successfully"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
