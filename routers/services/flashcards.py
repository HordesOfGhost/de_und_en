from fastapi import Request, APIRouter, Query, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from services.db import get_db
from routers.config import templates
import random

router = APIRouter()

@router.get("/flashcard", tags = ['flsashcard'], response_class=HTMLResponse, include_in_schema=False)
async def flashcard_page(
    request: Request,
    direction: str = Query("en_to_de"),
    db: Session = Depends(get_db)
):
    rows = db.execute(text("SELECT english, german FROM translations")).fetchall()
    if not rows:
        return templates.TemplateResponse("flashcard.html", {
            "request": request,
            "card": {"english": "", "german": ""},
            "direction": direction,
        })

    selected = random.choice(rows)
    card = {"english": selected[0], "german": selected[1]}

    return templates.TemplateResponse("flashcard.html", {
        "request": request,
        "card": card,
        "direction": direction,
    })
