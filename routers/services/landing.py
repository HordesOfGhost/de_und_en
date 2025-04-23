from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from routers.config import templates
from sqlalchemy.orm import Session
from services.db.models import get_db
from services.db.models import Translation
from sqlalchemy import func

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})

@router.get("/random-translations", tags=['random translation'])
def random_translations(db: Session = Depends(get_db)):
    results = db.query(Translation).order_by(func.random()).limit(5).all()
    return [{"english": t.english, "german": t.german} for t in results]