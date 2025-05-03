from fastapi import APIRouter
from services.db.models import init_db

router = APIRouter()

@router.on_event("startup")
async def on_startup():
    """
    Run initialization tasks on application startup.
    """
    init_db()
    print("Database initialized successfully.")


@router.on_event("shutdown")
def on_shutdown():
    """
    Perform cleanup tasks during shutdown.
    """
    print("Server is shutting down gracefully.")
