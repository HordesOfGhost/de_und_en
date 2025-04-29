from fastapi import APIRouter, Depends, HTTPException, Query, Form, Path
from sqlalchemy.orm import Session
from services.db.models import  get_db
from .config import get_model_and_schema_group
from schemas.enums import TableName

router = APIRouter()

@router.get("/records", tags=["crud"])
def read_records(
    table_name: TableName = Query(..., description="Select table"),
    db: Session = Depends(get_db)
):
    Model, group = get_model_and_schema_group(table_name)
    records = db.query(Model).all()

    if group == "bilingual":
        return [{"id": r.id, "english": r.english, "german": r.german} for r in records]
    elif group == "grammar":
        return [{"id": r.id, "german": r.german, "grammar_explanations": r.grammar_explanations} for r in records]

@router.get("/records/{record_id}", tags=["crud"])
def read_single_record(
    record_id: int,
    table_name: TableName = Query(..., description="Select table"),
    db: Session = Depends(get_db)
):
    Model, group = get_model_and_schema_group(table_name)
    record = db.query(Model).get(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    if group == "bilingual":
        return {"id": record.id, "english": record.english, "german": record.german}
    elif group == "grammar":
        return {"id": record.id, "german": record.german, "grammar_explanations": record.grammar_explanations}
