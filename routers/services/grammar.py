from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from routers.config import templates
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/grammar", tags=['grammar'], response_class=HTMLResponse, include_in_schema=False)
async def get_grammar_card(request: Request, direction: str = "en_to_de"):
    return templates.TemplateResponse("grammar.html", {"request": request, "direction":direction})

@router.post("/grammar", tags=['grammar'], response_class=JSONResponse)
async def get_german_grammar_explanations(german_sentences: str):
    grammar_explanations = get_grammar_explanations(german_sentences)
    return JSONResponse({
        "german":german_sentences,
        "grammar_explanations":grammar_explanations
    })