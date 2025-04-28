from fastapi import APIRouter, Request,Depends, Form
from fastapi.responses import HTMLResponse, JSONResponse
from services.conversation import generate_conversation_translate_and_save
from services.db import get_db
from sqlalchemy.orm import Session
from routers.config import templates

router = APIRouter()


@router.get("/conversation", tags=['conversation'], response_class=HTMLResponse, include_in_schema=False)
async def generate_conversation_page(request: Request):
    return templates.TemplateResponse("conversation.html", {"request": request})

@router.post("/conversation", tags=['conversation'])
async def generate_conversations(
    topic: str = Form(...),
    db: Session = Depends(get_db)
):
    eng_conversation, de_conversation, record_id = generate_conversation_translate_and_save(topic, db)
    
    # Return the conversations as JSON
    return JSONResponse({
        "id": record_id,
        "topic": topic,
        "english": eng_conversation,
        "german": de_conversation
    })

