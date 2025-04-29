from fastapi import APIRouter, Depends, HTTPException, Query, Form, Path
from sqlalchemy.orm import Session
from services.db.models import  get_db
from .config import get_model_and_schema_group
from schemas.enums import TableName

router = APIRouter()

@router.put("/records/{record_id}", tags=["crud"])
def update_record(
    record_id: int = Path(...),
    table_name: TableName = Query(..., description="Select table"),
    english: str = Form(None),
    german: str = Form(...),
    grammar_explanations: str = Form(None),
    db: Session = Depends(get_db)
):
    Model, group = get_model_and_schema_group(table_name)
    record = db.query(Model).get(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    if group == "bilingual":
        if english is None:
            raise HTTPException(status_code=400, detail="Missing 'english'")
        record.english = english
        record.german = german
    elif group == "grammar":
        if grammar_explanations is None:
            raise HTTPException(status_code=400, detail="Missing 'grammar_explanations'")
        record.german = german
        record.grammar_explanations = grammar_explanations

    db.commit()
    return {"message": f"Record {record_id} updated in {table_name}"}
