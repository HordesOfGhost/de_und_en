from fastapi import FastAPI
from routers import login, register, shutdown
from routers.events import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(login.router, prefix="/users", tags=["Users"])
app.include_router(register.router, prefix="/users", tags=["Users"])
app.include_router(shutdown.router, prefix="/events", tags=["Events"])


@app.get("/",tags=['Root'])
async def root():
    return {"message": "Welcome to the Language Learning API"}
