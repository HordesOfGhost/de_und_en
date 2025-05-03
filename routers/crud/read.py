from fastapi import (
    APIRouter, 
    HTTPException, 
    Query, 
    Path, 
    Depends,
    )
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from schemas.enums import TableName
from services.db.models import get_db
from .config import get_model_and_schema_group

router = APIRouter()

@router.get("/records", tags=["crud"])
def read_records(
    table_name: TableName = Query(..., description="Select the table to fetch records from."),
    db: Session = Depends(get_db)
):
    """
    Retrieve all records from the specified table.

    Parameters
    -----------
    table_name : TableName
        Enum value for the table name ('translations', 'conversations', or 'grammar').

    db : Session
        SQLAlchemy session dependency.

    Returns
    --------
    list[dict]
        A list of records formatted according to their group type.

    """
    try:
        Model, group = get_model_and_schema_group(table_name)
        records = db.query(Model).all()

        if group == "bilingual":
            return [{"id": r.id, "english": r.english, "german": r.german} for r in records]
        elif group == "grammar":
            return [{"id": r.id, "german": r.german, "grammar_explanations": r.grammar_explanations} for r in records]

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/records/{record_id}", tags=["crud"])
def read_single_record(
    record_id: int = Path(..., description="ID of the record to retrieve."),
    table_name: TableName = Query(..., description="Select the table to fetch the record from."),
    db: Session = Depends(get_db)
):
    """
    Retrieve a single record by ID from the specified table.

    Parameters
    -----------
    record_id : int
        The unique ID of the record.

    table_name : TableName
        Enum value for the table name ('translations', 'conversations', or 'grammar').

    db : Session
        SQLAlchemy session dependency.

    Returns
    --------
    dict
        A dictionary representation of the record.

    """
    try:
        Model, group = get_model_and_schema_group(table_name)
        record = db.query(Model).get(record_id)

        if not record:
            raise HTTPException(status_code=404, detail="Record not found")

        if group == "bilingual":
            return {"id": record.id, "english": record.english, "german": record.german}
        elif group == "grammar":
            return {"id": record.id, "german": record.german, "grammar_explanations": record.grammar_explanations}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
