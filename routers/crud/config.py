from fastapi import APIRouter, Depends, HTTPException, Query, Form, Path
from sqlalchemy.orm import Session
from services.db.models import Translation, Conversation, Grammar, get_db

router = APIRouter()

# Map table names to SQLAlchemy models
TABLE_MODEL_MAP = {
    "translations": Translation,
    "conversations": Conversation,
    "grammar": Grammar
}

# Map tables to schema group
TABLE_SCHEMA_GROUP = {
    "translations": "bilingual",
    "conversations": "bilingual",
    "grammar": "grammar"
}


def get_model_and_schema_group(table_name: str):
    model = TABLE_MODEL_MAP.get(table_name)
    group = TABLE_SCHEMA_GROUP.get(table_name)
    if not model or not group:
        raise HTTPException(status_code=400, detail="Invalid table name")
    return model, group
