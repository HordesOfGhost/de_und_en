from fastapi import APIRouter, Depends, HTTPException, Query, Path, Form
from sqlalchemy.orm import Session
from services.db.models import get_db
from services.db.utils import get_model
from enum import Enum

router = APIRouter()

class TableName(str, Enum):
    conversations = "conversations"
    translations = "translations"

@router.post("/records", tags=['crud'])
def create_record(
    table_name: TableName = Query(..., description="Choose 'conversations' or 'translations'"),
    english: str = Form(...),
    german: str = Form(...),
    db: Session = Depends(get_db)
):
    Model = get_model(table_name)
    record = Model(english=english, german=german)
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"message": "Record created", "record": {
        "id": record.id,
        "english": record.english,
        "german": record.german
    }}

@router.get("/records", tags=['crud'])
def read_records(
    table_name: TableName = Query(..., description="Choose 'conversations' or 'translations'"),
    db: Session = Depends(get_db)
):
    Model = get_model(table_name)
    records = db.query(Model).all()
    return [
        {"id": r.id, "english": r.english, "german": r.german}
        for r in records
    ]

@router.get("/records/{record_id}", tags=['crud'])
def read_single_record(
    record_id: int,
    table_name: TableName = Query(..., description="Choose 'conversations' or 'translations'"),
    db: Session = Depends(get_db)
):
    Model = get_model(table_name)
    record = db.query(Model).get(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"id": record.id, "english": record.english, "german": record.german}

@router.put("/records/{record_id}", tags=['crud'])
def update_record(
    record_id: int = Path(...),
    table_name: TableName = Query(..., description="Choose 'conversations' or 'translations'"),
    english: str = Form(...),
    german: str = Form(...),
    db: Session = Depends(get_db)
):
    Model = get_model(table_name)
    record = db.query(Model).get(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    record.english = english
    record.german = german
    db.commit()
    db.refresh(record)
    return {"message": f"Record {record_id} updated", "record": {
        "id": record.id,
        "english": record.english,
        "german": record.german
    }}

@router.delete("/records/{record_id}", tags=['crud'])
def delete_record(
    record_id: int,
    table_name: TableName = Query(..., description="Choose 'conversations' or 'translations'"),
    db: Session = Depends(get_db)
):
    Model = get_model(table_name)
    record = db.query(Model).get(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    db.delete(record)
    db.commit()
    return {"message": f"Deleted record {record_id} from {table_name}"}
