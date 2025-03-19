import signal
import os
from fastapi import APIRouter, Response

router = APIRouter()

def graceful_shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    return Response(status_code=200, content='Server shutting down...')

@router.on_event('shutdown')
def on_shutdown():
    print('Server shutting down...')
