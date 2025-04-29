from fastapi import APIRouter, Depends, HTTPException, Query, Form, Path
from sqlalchemy.orm import Session
from services.db.models import get_db
from .config import get_model_and_schema_group
from schemas.enums import TableName
router = APIRouter()

@router.post("/records", tags=["crud"])
def create_record(
    table_name: TableName = Query(..., description="Select table"),
    english: str = Form(None),
    german: str = Form(...),
    grammar_explanations: str = Form(None),
    db: Session = Depends(get_db)
):
    Model, group = get_model_and_schema_group(table_name)

    if group == "bilingual":
        if english is None:
            raise HTTPException(status_code=400, detail="Missing 'english'")
        record = Model(english=english, german=german)
    elif group == "grammar":
        if grammar_explanations is None:
            raise HTTPException(status_code=400, detail="Missing 'grammar_explanations'")
        record = Model(german=german, grammar_explanations=grammar_explanations)
    else:
        raise HTTPException(status_code=400, detail="Unsupported schema group")

    db.add(record)
    db.commit()
    db.refresh(record)
    return {"message": f"Record created in {table_name}", "id": record.id}
