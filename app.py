from fastapi import FastAPI
from routers.services import (
    translate,
    transcribe,
    flashcards,
    synthesize,
    conversation,
    landing,
    ocr,
    grammar,
)
from routers.events import events
from routers.crud import (
    create,
    read,
    update,
    delete
)
from fastapi.staticfiles import StaticFiles
from pathlib import Path


app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
    name="static",
)

app.include_router(translate.router)
app.include_router(transcribe.router)
app.include_router(events.router)
app.include_router(flashcards.router)
app.include_router(synthesize.router)
app.include_router(conversation.router)
app.include_router(grammar.router)
app.include_router(ocr.router)
app.include_router(landing.router)
app.include_router(create.router)
app.include_router(read.router)
app.include_router(update.router)
app.include_router(delete.router)





