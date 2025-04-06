from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from .config import templates

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})
