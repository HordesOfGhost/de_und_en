from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from routers.config import templates
from fastapi.templating import Jinja2Templates
from services.grammar.explain import explain_and_save_grammar_for_german_sentences
from services.db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/grammar", tags=['grammar'], response_class=HTMLResponse, include_in_schema=False)
async def get_grammar_card(request: Request, direction: str = "en_to_de"):
    return templates.TemplateResponse("grammar.html", {"request": request, "direction":direction})

@router.post("/grammar", tags=['grammar'], response_class=JSONResponse)
async def get_german_grammar_explanations(german_sentences: str=Form(...), db: Session = Depends(get_db)):
    grammar_explanations, record_id = explain_and_save_grammar_for_german_sentences(german_sentences, db)
    return JSONResponse({
        "id":record_id,
        "german":german_sentences,
        "grammar_explanations":grammar_explanations
    })