from fastapi import FastAPI
from routers import events, landing, translate, transcribe, flashcards

app = FastAPI()

app.include_router(events.router)
app.include_router(landing.router)
app.include_router(translate.router)
app.include_router(transcribe.router)
app.include_router(flashcards.router)


