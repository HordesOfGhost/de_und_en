from fastapi import (
    APIRouter, 
    Request,
    )
from fastapi.responses import (
    JSONResponse, 
    Response,
    )
from services.tts import (
    synthesize_text, 
    synthesize_conversation,
    )

router = APIRouter()

@router.post("/synthesize", tags=['synthesize'])
async def synthesize(request: Request):
    """
    Endpoint for synthesizing text into speech.

    Receives a JSON body with text and optional language.
    Synthesizes the text into speech and returns it as an audio file.

    Parameters
    -----------
    request : Request
        The incoming HTTP request, containing a JSON body with the text and language.

    Returns
    --------
    Response
        The synthesized speech as a .wav audio file.
    """
    try:
        body = await request.json()  
        
        text = body.get("text")  
        language = body.get("language", "en")  

        if not text:
            raise JSONResponse(
                status_code=400, 
                content={"error": "Text not provided in request body"
            })

        wav_bytes = synthesize_text(text, language)
        return Response(
            content=wav_bytes, 
            media_type="audio/wav"
        )

    except Exception as e:

        return JSONResponse(
            status_code=500, 
            content={"error": str(e)}
        )

    
@router.post("/synthesize-conversation", tags=['synthesize'], include_in_schema=False)
async def synthesize_conversations(request: Request):
    """
    Endpoint for synthesizing a conversation into speech.

    Receives a JSON body with a conversation (list of sentences) and optional language.
    Synthesizes the conversation into speech and returns it as an audio file.

    Parameters
    -----------
    request : Request
        The incoming HTTP request, containing a JSON body with the conversation and language.

    Returns
    --------
    Response
        The synthesized conversation as a .wav audio file.
    """
    try:
        body = await request.json()

        conversation = body.get("conversation")  
        language = body.get("language", "en")  

        if not conversation:
            return JSONResponse(
                status_code=400, 
                content={"error": "Conversation not provided in request body"}
            )

        wav_bytes = synthesize_conversation(conversation, language)
        return Response(
            content=wav_bytes, 
            media_type="audio/wav"
        )

    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={"error": str(e)}
        )
