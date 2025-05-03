from fastapi import (
    APIRouter, 
    HTTPException, 
    Depends, 
    Query, 
    Path,
    )
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from schemas.enums import TableName
from services.db.models import get_db
from .config import get_model_and_schema_group

router = APIRouter()

@router.delete("/records/{record_id}", tags=["crud"])
def delete_record(
    record_id: int = Path(..., description="ID of the record to delete."),
    table_name: TableName = Query(..., description="Select the table to delete from."),
    db: Session = Depends(get_db)
):
    """
    Delete a record from the specified table by its ID.

    Parameters
    -----------
    record_id : int
        The ID of the record to delete.

    table_name : TableName
        Enum specifying the table name ('translations', 'conversations', or 'grammar').

    db : Session
        SQLAlchemy session (injected by FastAPI).

    Returns
    --------
    dict
        A message confirming successful deletion.

    """
    try:
        Model, _ = get_model_and_schema_group(table_name)
        record = db.query(Model).get(record_id)

        if not record:
            raise HTTPException(status_code=404, detail="Record not found")

        db.delete(record)
        db.commit()

        return {"message": f"Deleted record {record_id} from '{table_name}'."}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
