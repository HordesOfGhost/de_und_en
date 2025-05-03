from services.models import gemini_model
from .prompt import get_prompt_for_generating_listening_content
from sqlalchemy.orm import Session
from .utils import extract_json_content_from_llm_response
from schemas.metadata import ListeningMetaDataModel
from services.db.crud_for_services import save_listening_metadata

def generate_listening_content_and_save_metadata(level: str, db: Session):
    """
    Generates a listening comprehension task and stores its metadata in the database.

    Uses a language model to generate listening content based on the provided difficulty level.
    The resulting JSON includes an article and topic metadata, which is saved to the database.
    The article text is cleaned before returning.

    Parameters:
    -----------
    level : str
        The CEFR difficulty level (e.g., A1, B1, C2) for the listening content.
    db : Session
        SQLAlchemy session object used to interact with the database.

    Returns:
    --------
    dict
        A dictionary containing the generated listening content, including the article, topic, and level.
    """
    prompt = get_prompt_for_generating_listening_content(level, db)
    response = gemini_model.generate_content(prompt).text
    json_response = extract_json_content_from_llm_response(response)
    json_response['article'] = json_response['article'].replace("\n", "")
    
    listening_metadata_data = ListeningMetaDataModel(
        level=json_response['level'],
        topic=json_response['topic']
    )
    save_listening_metadata(db, listening_metadata_data=listening_metadata_data)
    return json_response
