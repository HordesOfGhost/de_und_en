from sqlalchemy.orm import Session
from services.db.schemas import ConversationModel
from services.db.crud import save_conversation
from .utils import translate_lng, add_newline_before_speaker

def translate_conversation_and_save(input_text: str, db: Session):
    
    translated_text = translate_lng(input_text, target_language = "de")
    # translated_text = add_newline_before_speaker(translated_text)

    translation_data = ConversationModel(
        english=input_text,
        german=translated_text
    )
    saved_translation = save_conversation(db, translation_data)
    return translated_text, saved_translation
