from fastapi import FastAPI
from contextlib import asynccontextmanager
from services.database import create_user_table

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown events."""
    create_user_table()  
    yield 
    print("Server shutting down... Heee")
