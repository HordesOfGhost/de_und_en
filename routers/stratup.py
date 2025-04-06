from fastapi import APIRouter
from services.db.models import init_db

router = APIRouter()

@router.on_event("startup")
async def on_startup():
    init_db()
