from fastapi import FastAPI
from routers import landing, translate, stratup

app = FastAPI()

app.include_router(stratup.router)
app.include_router(landing.router)
app.include_router(translate.router)


