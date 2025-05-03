from fastapi import (
    APIRouter, 
    Request, 
    HTTPException,
    Depends,
    )
from services.db.models import(
    get_db, 
    Translation,    
    )
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from routers.config import templates

router = APIRouter()

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def landing(request: Request):
    """
    Renders the landing page.

    Parameters:
    -----------
    request : Request
        The incoming HTTP request object for rendering HTML.

    Returns:
    --------
    HTMLResponse
        Renders the landing template.
    """
    return templates.TemplateResponse("landing.html", {
        "request": request
    })

@router.get("/random-translations", tags=['random translation'])
def random_translations(db: Session = Depends(get_db), limit: int = 5):
    """
    Fetches a random set of translations from the 'Translation' table.

    Parameters
    -----------
    db : Session
        SQLAlchemy database session dependency.
    limit : int
        The number of random translations to return (default: 5).

    Returns
    --------
    List[Dict[str, str]]
        A list of dictionaries containing English and German translations.
    
    """
    try:
        results = db.query(Translation).order_by(func.random()).limit(limit).all()

        if not results:
            raise HTTPException(
                status_code=404, 
                detail="No translations found."
            )

        return [{"english": t.english, "german": t.german} for t in results]

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error fetching random translations: {str(e)}"
        )
