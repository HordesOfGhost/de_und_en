from services.models import gemini_model
from .prompt import get_prompt_for_generating_writing_content
from sqlalchemy.orm import Session
from .utils import extract_json_content_from_llm_response


def generate_writing_topic(level: str, db: Session):
    """
    Generates a writing topic based on the specified level.

    This function constructs a prompt to generate a writing topic using the Gemini model 
    based on the provided level (e.g., beginner, intermediate, advanced). The generated 
    response is parsed and returned as a structured JSON object.

    Parameters:
    -----------
    level : str
        The writing level (e.g., "beginner", "intermediate", "advanced") used to generate 
        the writing topic. This helps tailor the topic generation to the user's proficiency.
    
    db : Session
        The database session used for potential database interactions (e.g., logging, 
        storing metadata).

    Returns:
    --------
    dict
        The parsed JSON response containing the generated writing topic and any related metadata.

    Example:
    --------
    level = "intermediate"
    writing_topic = generate_writing_topic(level, db)
    print(writing_topic)
    """
    
    prompt = get_prompt_for_generating_writing_content(level, db)
    response = gemini_model.generate_content(prompt).text
    json_response = extract_json_content_from_llm_response(response)
    return json_response
