from fastapi import APIRouter, Request,Depends, Form
from services.conversation import generate_conversation_translate_and_save
from services.db import get_db
from sqlalchemy.orm import Session
from routers.config import templates

router = APIRouter()


@router.get("/conversation")
async def generate_conversation(request: Request):
    return templates.TemplateResponse("conversation.html", {"request": request})

@router.post("/conversation")
def generate_conversations(request: Request, topic: str = Form(...), db: Session = Depends(get_db)):
    eng_conversation, de_conversation = generate_conversation_translate_and_save(topic, db)
    return templates.TemplateResponse("conversation.html", {
        "request": request,
        "topic": topic,
        "english": eng_conversation,
        "german": de_conversation
    })


