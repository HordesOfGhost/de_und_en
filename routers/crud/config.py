from fastapi import HTTPException
from typing import Tuple, Type
from services.db.models import Translation, Conversation, Grammar

TABLE_MODEL_MAP = {
    "translations": Translation,
    "conversations": Conversation,
    "grammar": Grammar
}

TABLE_SCHEMA_GROUP = {
    "translations": "bilingual",
    "conversations": "bilingual",
    "grammar": "grammar"
}


def get_model_and_schema_group(table_name: str) -> Tuple[Type, str]:
    """
    Retrieve the model class and schema group associated with a given table name.

    Parameters
    -----------
    table_name : str
        The name of the table (e.g., 'translations', 'conversations', or 'grammar').

    Returns
    --------
    Tuple[Type, str]
        A tuple containing the ORM model class and the schema group name.

    Raises
    -------
    HTTPException
        If the table name is not recognized or mapped.
    """
    try:
        model = TABLE_MODEL_MAP[table_name]
        group = TABLE_SCHEMA_GROUP[table_name]
        return model, group
    except KeyError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid table name: '{table_name}'. Must be one of: {list(TABLE_MODEL_MAP.keys())}"
        )
