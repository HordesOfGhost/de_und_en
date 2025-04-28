from sqlalchemy.orm import Session
from schemas.conversation import ConversationModel
from services.db.crud_for_services import save_conversation
from .utils import translate_lng_with_gemini, add_newline_before_speaker

def translate_conversation_and_save_with_gemini(input_text: str, db: Session):
    
    translated_text = translate_lng_with_gemini(input_text, target_language = "de")
    # translated_text = add_newline_before_speaker(translated_text)

    translation_data = ConversationModel(
        english=input_text,
        german=translated_text
    )
    saved_conversation = save_conversation(db, translation_data)
    return translated_text, saved_conversation
