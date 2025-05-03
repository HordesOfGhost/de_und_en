from fastapi import (
    APIRouter, 
    Request, 
    HTTPException,
    Form, 
    Depends, 
    )
from fastapi.responses import (
    HTMLResponse, 
    JSONResponse,
    )
from sqlalchemy.orm import Session
from routers.config import templates
from services.grammar.explain import explain_and_save_grammar_for_german_sentences
from services.db import get_db

router = APIRouter()

@router.get("/grammar", tags=['grammar'], response_class=HTMLResponse, include_in_schema=False)
async def render_grammar_expanations_page(request: Request, direction: str = "en_to_de"):
    """
    Serve the grammar explanation page for German sentences.

    Parameters
    -----------
    request : Request
        The incoming HTTP request object for rendering HTML.
    direction : str
        The direction of translation (e.g., 'en_to_de'). Defaults to 'en_to_de'.

    Returns
    --------
    HTMLResponse
        Renders the grammar explanation template.
    """
    return templates.TemplateResponse("grammar.html", {
        "request": request, 
        "direction": direction
    })

@router.post("/grammar", tags=['grammar'], response_class=JSONResponse)
async def get_german_grammar_explanations(
    german_sentences: str = Form(..., description="German sentences to explain grammar for."),
    db: Session = Depends(get_db)
):
    """
    Accept German sentences, explain their grammar, and store the explanations.

    Parameters
    -----------
    german_sentences : str
        The German sentences for which grammar explanations are to be generated.
    db : Session
        SQLAlchemy database session dependency.

    Returns
    --------
    JSONResponse
        The generated grammar explanations along with the German sentences and record ID.

    """
    try:
        grammar_explanations, record_id = explain_and_save_grammar_for_german_sentences(german_sentences, db)

        return JSONResponse({
            "id": record_id,
            "german": german_sentences,
            "grammar_explanations": grammar_explanations
        })

    except ValueError as ve:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid input: {str(ve)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error explaining grammar: {str(e)}"
        )
