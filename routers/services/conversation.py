from fastapi import(
    APIRouter, 
    Request, 
    HTTPException, 
    Depends, 
    Form,
    )
from fastapi.responses import( 
    HTMLResponse, 
    JSONResponse,
    )
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from routers.config import templates
from services.conversation import generate_conversation_translate_and_save
from services.db import get_db

router = APIRouter()

@router.get("/conversation", tags=['conversation'], response_class=HTMLResponse, include_in_schema=False)
async def render_conversation_page(request: Request):
    """
    Serve the conversation generator HTML page.

    Parameters
    -----------
    request : Request
        The incoming HTTP request object.

    Returns
    --------
    HTMLResponse
        Renders the conversation.html template.
    """
    return templates.TemplateResponse("conversation.html", {
        "request": request
    })


@router.post("/conversation", tags=['conversation'])
async def generate_conversations(
    topic: str = Form(..., description="Topic to generate a bilingual conversation about."),
    db: Session = Depends(get_db)
):
    """
    Generate a conversation based on a given topic, translate it into German,
    save both versions to the database, and return them.

    Parameters
    -----------
    topic : str
        The topic for the conversation.
    db : Session
        SQLAlchemy database session dependency.

    Returns
    --------
    JSONResponse
        JSON containing the English and German conversation, and the database record ID.

    """
    try:
        eng_conversation, de_conversation, record_id = generate_conversation_translate_and_save(topic, db)

        return JSONResponse({
            "id": record_id,
            "topic": topic,
            "english": eng_conversation,
            "german": de_conversation
        })

    except SQLAlchemyError as db_err:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Database error: {str(db_err)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate conversation: {str(e)}"
        )
