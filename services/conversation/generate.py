from sqlalchemy.orm import Session
from services.models import gemini_model
from .prompt import get_conversation_prompt
from services.translation import translate_conversation_and_save_with_gemini

def generate_conversation_translate_and_save(topic: str, db: Session):
    """
    Generates a conversation based on the given topic, translates it, and saves the result.
    
    Parameters
    -----------
    topic: str
        The topic to base the conversation on.
    db: Session
        The database session for saving the conversation.
    
    Returns
    --------
    Tuple[str, str, int]
        A tuple containing the English conversation, German conversation, and the saved conversation ID.
    """
    try:
        prompt = get_conversation_prompt(topic)
        english_conversation = gemini_model.generate_content(prompt).text
        english_conversation = english_conversation.replace("*", "")
        german_conversation, saved_conversation = translate_conversation_and_save_with_gemini(english_conversation, db)
        return english_conversation, german_conversation, saved_conversation.id
    
    except Exception as e:
        raise
