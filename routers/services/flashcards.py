from fastapi import (
    APIRouter, 
    Request, 
    HTTPException, 
    Query, 
    Depends,
    )
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from routers.config import templates
import random
from sqlalchemy import text
from services.db import get_db

router = APIRouter()

@router.get("/flashcard", tags=['flashcard'], response_class=HTMLResponse, include_in_schema=False)
async def render_flashcard_page(
    request: Request,
    direction: str = Query("en_to_de", description="Direction of translation, e.g., 'en_to_de' or 'de_to_en'"),
    db: Session = Depends(get_db)
):
    """
    Display a flashcard with a random translation pair from the database.

    This endpoint serves a flashcard with the translation from English to German
    or vice versa based on the direction parameter.

    Parameters
    -----------
    request : Request
        The incoming HTTP request object (for rendering HTML).
    direction : str
        The translation direction. Defaults to 'en_to_de'.
    db : Session
        SQLAlchemy database session dependency.

    Returns
    --------
    HTMLResponse
        The rendered flashcard page with the selected card and translation direction.

    """
    try:
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

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error fetching flashcard data: {str(e)}"
        )
