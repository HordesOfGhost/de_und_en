from services.models import gemini_model
from .prompt import get_prompt_for_generating_reading_content
from sqlalchemy.orm import Session
from .utils import extract_json_content_from_llm_response
from schemas.metadata import ReadingMetaDataModel
from services.db.crud_for_services import save_reading_metadata

def generate_reading_content_and_save_metadata(level: str, db: Session):
    """
    Generates reading content using an LLM and saves associated metadata to the database.

    Constructs a prompt for generating reading content based on the CEFR level.
    Sends the prompt to the Gemini model, extracts the JSON response, and stores the level and topic
    as metadata in the database.

    Parameters:
    -----------
    level : str
        CEFR level for the desired reading content (e.g., "A1", "B2").
    db : Session
        SQLAlchemy database session used to save the metadata.

    Returns:
    --------
    dict
        The parsed JSON response containing reading content, questions, answers, level, and topic.
    """
    prompt = get_prompt_for_generating_reading_content(level, db)
    response = gemini_model.generate_content(prompt).text
    json_response = extract_json_content_from_llm_response(response)
    reading_metadata_data = ReadingMetaDataModel(
        level=json_response['level'],
        topic=json_response['topic']
    )
    save_reading_metadata(db, reading_metadata_data=reading_metadata_data)
    return json_response