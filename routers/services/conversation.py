from fastapi import APIRouter, Request,Depends, Form
from fastapi.responses import HTMLResponse
from services.conversation import generate_conversation_translate_and_save
from services.db import get_db
from sqlalchemy.orm import Session
from routers.config import templates

router = APIRouter()


@router.get("/conversation", tags=['conversation'], response_class=HTMLResponse)
async def generate_conversation_page(request: Request):
    return templates.TemplateResponse("conversation.html", {"request": request})

@router.post("/conversation", tags = ['conversation'], response_class=HTMLResponse)
def generate_conversations(request: Request, topic: str = Form(...), db: Session = Depends(get_db)):
    eng_conversation, de_conversation = generate_conversation_translate_and_save(topic, db)
    return templates.TemplateResponse("conversation.html", {
        "request": request,
        "topic": topic,
        "english": eng_conversation,
        "german": de_conversation
    })


