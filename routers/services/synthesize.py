from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse, Response
from services.tts import synthesize_text, synthesize_conversation

router = APIRouter()

@router.get("/synthesize")
async def synthesize_translations(text: str = Query(...), language: str = Query(...)):
    try:
        wav_bytes = synthesize_text(text, language)
        return Response(content=wav_bytes, media_type="audio/wav")
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/synthesize-conversation")
def synthesize_conversations(conversation: str = Query(...), language: str = Query(...)):
    try:
        wav_bytes = synthesize_conversation(conversation, language)
        return Response(content=wav_bytes, media_type="audio/wav")
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
