from fastapi import APIRouter, Response
from services.db.models import init_db
import os
import signal
router = APIRouter()

@router.on_event("startup")
async def on_startup():
    init_db()

 
def graceful_shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    return Response(status_code=200, content='Server shutting down...')
 
@router.on_event('shutdown')
def on_shutdown():
    print('Server shutting down...')
    graceful_shutdown()