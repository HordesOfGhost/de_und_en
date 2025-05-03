from services.db.models import Conversation, Translation
from fastapi import HTTPException
from sqlalchemy.orm import Session

def get_model(table_name: str):
    """
    Retrieve the SQLAlchemy model class for the given table name.

    Parameters
    -----------
    table_name: str
        The name of the table to retrieve the model for.
    
    Returns
    --------
    model class
        The SQLAlchemy model corresponding to the provided table name.
    """
    if table_name == "conversations":
        return Conversation
    elif table_name == "translations":
        return Translation
    else:
        raise HTTPException(status_code=400, detail="Invalid table name")

def save_if_not_exists(db: Session, model_class, filter_by_kwargs, data_to_save):
    """
    Generic function to save an entry if it does not exist.

    Parameters
    -----------
    db: Session
        The SQLAlchemy session object.
    model_class: Type[Base]
        The model class (Translation, Grammar, etc.).
    filter_by_kwargs: dict
        A dictionary of the fields to filter by in the model.
    data_to_save: dict
        The data to save if the record does not exist.

    Returns
    --------
    The existing or newly created model instance.
    """
    existing_record = db.query(model_class).filter_by(**filter_by_kwargs).first()

    if existing_record:
        return existing_record

    record = model_class(**data_to_save)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record