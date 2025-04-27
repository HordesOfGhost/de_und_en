from fastapi import FastAPI
from routers.services import (
    translate,
    transcribe,
    flashcards,
    synthesize,
    conversation,
    landing,
    ocr,
)
from routers.events import events
from routers.crud import api
from fastapi.staticfiles import StaticFiles
from pathlib import Path


app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
    name="static",
)


app.include_router(events.router)
app.include_router(landing.router)
app.include_router(translate.router)
app.include_router(transcribe.router)
app.include_router(flashcards.router)
app.include_router(synthesize.router)
app.include_router(conversation.router)
app.include_router(api.router)
app.include_router(ocr.router)




