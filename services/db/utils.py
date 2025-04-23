from services.db.models import Conversation, Translation
from fastapi import HTTPException

def get_model(table_name: str):
    if table_name == "conversations":
        return Conversation
    elif table_name == "translations":
        return Translation
    else:
        raise HTTPException(status_code=400, detail="Invalid table name")
