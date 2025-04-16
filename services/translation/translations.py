from sqlalchemy.orm import Session
from services.db.schemas import TranslationModel
from services.db.crud import save_translation
from services.tts import synthesize_text
from .utils import translate_lng

### Legacy function with Madlad
def translate_translation_and_save_legacy(input_text: str, direction: str, db: Session):

    if direction == "en_to_de":
        translated_text = translate_lng(input_text, target_language = "2de")
        synthesize_text(input_text,"en")
        synthesize_text(translated_text,"de")
    elif direction == "de_to_en":
        translated_text = translate_lng(input_text, target_language = "2en")
        synthesize_text(input_text,"de")
        synthesize_text(translated_text,"en")

    translation_data = TranslationModel(
        english=input_text if direction == "en_to_de" else translated_text,
        german=translated_text if direction == "en_to_de" else input_text
    )
    saved_translation = save_translation(db, translation_data)
    return translated_text, saved_translation

def translate_translation_and_save(input_text: str, direction: str, db: Session):

    if direction == "en_to_de":
        translated_text = translate_lng(input_text, target_language = "de")
        synthesize_text(input_text,"en")
        synthesize_text(translated_text,"de")
    elif direction == "de_to_en":
        translated_text = translate_lng(input_text, target_language = "en")
        synthesize_text(input_text,"de")
        synthesize_text(translated_text,"en")

    translation_data = TranslationModel(
        english=input_text if direction == "en_to_de" else translated_text,
        german=translated_text if direction == "en_to_de" else input_text
    )
    saved_translation = save_translation(db, translation_data)
    return translated_text, saved_translation

