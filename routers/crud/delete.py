from fastapi import APIRouter, Depends, HTTPException, Query, Form, Path
from sqlalchemy.orm import Session
from services.db.models import  Grammar, get_db
from .config import get_model_and_schema_group
from schemas.enums import TableName

router = APIRouter()

@router.delete("/records/{record_id}", tags=["crud"])
def delete_record(
    record_id: int,
    table_name: TableName = Query(..., description="Select table"),
    db: Session = Depends(get_db)
):
    Model, _ = get_model_and_schema_group(table_name)
    record = db.query(Model).get(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    db.delete(record)
    db.commit()
    return {"message": f"Deleted record {record_id} from {table_name}"}
