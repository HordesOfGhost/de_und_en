from sqlalchemy.orm import Session
from schemas.translation import TranslationModel
from services.db.crud_for_services import save_translation
from services.tts import synthesize_text
from .utils import translate_lng_with_gemini, translate_lng_with_madlad

### Legacy function with Madlad
def translate_translation_and_save_with_madlad(input_text: str, direction: str, db: Session):
    """
    Translates a text between English and German using Madlad, synthesizes speech for both languages, and saves the translation to the database.

    This function uses the Madlad model to translate text from English to German or vice versa.
    After translation, it synthesizes speech for the original and translated texts in the respective languages.
    It then stores both the original and translated texts in the database.

    Parameters
    -----------
    input_text : str
        The text to be translated.
    direction : str
        The direction of translation: "en_to_de" for English to German, "de_to_en" for German to English.
    db : Session
        The SQLAlchemy database session used to persist the translation data.

    Returns
    --------
    Tuple[str, int]
        A tuple containing the translated text and the ID of the saved translation in the database.
    """

    if direction == "en_to_de":
        translated_text = translate_lng_with_madlad(input_text, target_language = "2de")
        synthesize_text(input_text,"en")
        synthesize_text(translated_text,"de")
    elif direction == "de_to_en":
        translated_text = translate_lng_with_madlad(input_text, target_language = "2en")
        synthesize_text(input_text,"de")
        synthesize_text(translated_text,"en")

    translation_data = TranslationModel(
        english=input_text if direction == "en_to_de" else translated_text,
        german=translated_text if direction == "en_to_de" else input_text
    )
    saved_translation = save_translation(db, translation_data)
    return translated_text, saved_translation.id

def translate_translation_and_save_with_gemini(input_text: str, direction: str, db: Session):
    """
    Translates a text between English and German using Gemini, synthesizes speech for both languages, and saves the translation to the database.

    This function uses the Gemini model to translate text from English to German or vice versa.
    After translation, it synthesizes speech for the original and translated texts in the respective languages.
    It then stores both the original and translated texts in the database.

    Parameters
    -----------
    input_text : str
        The text to be translated.
    direction : str
        The direction of translation: "en_to_de" for English to German, "de_to_en" for German to English.
    db : Session
        The SQLAlchemy database session used to persist the translation data.

    Returns
    --------
    Tuple[str, int]
        A tuple containing the translated text and the ID of the saved translation in the database.
    """

    if direction == "en_to_de":
        translated_text = translate_lng_with_gemini(input_text, target_language = "de")
        synthesize_text(input_text,"en")
        synthesize_text(translated_text,"de")
    elif direction == "de_to_en":
        translated_text = translate_lng_with_gemini(input_text, target_language = "en")
        synthesize_text(input_text,"de")
        synthesize_text(translated_text,"en")

    translation_data = TranslationModel(
        english=input_text if direction == "en_to_de" else translated_text,
        german=translated_text if direction == "en_to_de" else input_text
    )
    saved_translation = save_translation(db, translation_data)
    return translated_text, saved_translation.id

