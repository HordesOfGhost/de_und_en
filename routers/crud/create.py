from fastapi import (
    APIRouter, 
    HTTPException, 
    Query, 
    Form, 
    Depends
    )
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from schemas.enums import TableName
from services.db.models import get_db
from .config import get_model_and_schema_group

router = APIRouter()

@router.post("/records", tags=["crud"])
def create_record(
    table_name: TableName = Query(..., description="Target table to insert into."),
    english: str = Form(None),
    german: str = Form(..., description="German translation or explanation."),
    grammar_explanations: str = Form(None),
    db: Session = Depends(get_db)
):
    """
    Create a new record in the specified table.

    Parameters
    -----------
    table_name : TableName
        The name of the table to insert the record into (must be one of 'translations', 'conversations', 'grammar').

    english : str, optional
        Required if the table group is 'bilingual'.

    german : str
        Required for all records. Represents either the translation or grammar text.

    grammar_explanations : str, optional
        Required if the table group is 'grammar'.

    db : Session
        SQLAlchemy session dependency.

    Returns
    --------
    dict
        A success message with the new record's ID.

    """
    try:
        Model, group = get_model_and_schema_group(table_name)

        if group == "bilingual":
            if english is None:
                raise HTTPException(status_code=400, detail="Missing 'english' field for bilingual record.")
            record = Model(english=english, german=german)

        elif group == "grammar":
            if grammar_explanations is None:
                raise HTTPException(status_code=400, detail="Missing 'grammar_explanations' for grammar record.")
            record = Model(german=german, grammar_explanations=grammar_explanations)

        else:
            raise HTTPException(status_code=400, detail="Unsupported schema group.")

        db.add(record)
        db.commit()
        db.refresh(record)

        return {
            "message": f"Record created in '{table_name}'.",
            "id": record.id
        }

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
