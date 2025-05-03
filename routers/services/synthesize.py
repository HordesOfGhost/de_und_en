from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse, Response
from services.tts import synthesize_text, synthesize_conversation

router = APIRouter()

@router.post("/synthesize", tags=['synthesize'])
async def synthesize(request: Request):
    try:
        body = await request.json()  # Parse the JSON body
        
        text = body.get("text")  # Get text from the body
        language = body.get("language", "en")  # Default to 'en' if not specified

        if not text:
            return JSONResponse(status_code=400, content={"error": "Text not provided in request body"})

        wav_bytes = synthesize_text(text, language)
        return Response(content=wav_bytes, media_type="audio/wav")

    except Exception as e:
        # Log the error details for debugging
        print(f"Error during synthesis: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

    
@router.post("/synthesize-conversation", tags=['synthesize'], include_in_schema=False)
async def synthesize_conversations(request: Request):
    try:
        body = await request.json()

        conversation = body.get("conversation")
        language = body.get("language", "en")

        if not conversation:
            return JSONResponse(status_code=400, content={"error": "Conversation not provided in request body"})

        wav_bytes = synthesize_conversation(conversation, language)
        return Response(content=wav_bytes, media_type="audio/wav")

    except Exception as e:
        print(f"Error during synthesis: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
