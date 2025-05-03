from fastapi import (
    APIRouter, 
    HTTPException, 
    Query, 
    Form, 
    Path, 
    Depends,
    )
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from schemas.enums import TableName
from services.db.models import  get_db
from .config import get_model_and_schema_group

router = APIRouter()

@router.put("/records/{record_id}", tags=["crud"])
def update_record(
    record_id: int = Path(..., description="ID of the record to update"),
    table_name: TableName = Query(..., description="Target table name"),
    english: str = Form(None),
    german: str = Form(..., description="German translation or explanation"),
    grammar_explanations: str = Form(None),
    db: Session = Depends(get_db)
):
    """
    Updates a record in the specified table based on the record ID and schema group.

    Parameters
    -----------
    record_id : int
        The ID of the record to update.

    table_name : TableName
        The name of the table (must be 'translations', 'conversations', or 'grammar').

    english : str, optional
        The English translation (required for bilingual records).

    german : str
        The German translation or grammar explanation (required for all records).

    grammar_explanations : str, optional
        The grammar explanation (required for grammar records).

    db : Session
        SQLAlchemy database session (injected by FastAPI).

    Returns
    --------
    dict
        A confirmation message on successful update.
        
    """
    try:
        Model, group = get_model_and_schema_group(table_name)
        record = db.query(Model).get(record_id)

        if not record:
            raise HTTPException(status_code=404, detail="Record not found")

        if group == "bilingual":
            if english is None:
                raise HTTPException(status_code=400, detail="Missing 'english' field for bilingual record.")
            record.english = english
            record.german = german

        elif group == "grammar":
            if grammar_explanations is None:
                raise HTTPException(status_code=400, detail="Missing 'grammar_explanations' for grammar record.")
            record.german = german
            record.grammar_explanations = grammar_explanations

        db.commit()
        return {"message": f"Record {record_id} updated in '{table_name}'."}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
