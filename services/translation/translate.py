from services.models import madlad_model, madlad_tokenizer, device
from services.utils import split_sentences
from sqlalchemy.orm import Session
from services.db.schemas import TranslationModel
from services.db.crud import save_translation


def convert_to_de(input_text):

    sentences = split_sentences(input_text)

    translated_sentences = " "

    for sentence in sentences:
        inputs = madlad_tokenizer(f"<2de> {sentence}", return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # Generate output
        outputs = madlad_model.generate(**inputs)

        # Decode
        decoded_sentence = madlad_tokenizer.batch_decode(outputs, skip_special_tokens=True)

        translated_sentences += " " + decoded_sentence[0]
    
    return translated_sentences.strip()

def convert_to_en(input_text):
    sentences = split_sentences(input_text)
    translated_sentences = " "

    for sentence in sentences:
        inputs = madlad_tokenizer(f"<2en> {sentence}", return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # Generate output
        outputs = madlad_model.generate(**inputs)

        # Decode
        decoded_sentence = madlad_tokenizer.batch_decode(outputs, skip_special_tokens=True)

        translated_sentences += " " + decoded_sentence[0]
    
    return translated_sentences.strip()

def translate_and_save(input_text: str, direction: str, db: Session):

    if direction == "en_to_de":
        translated_text = convert_to_de(input_text)
    else:
        translated_text = convert_to_en(input_text)

    translation_data = TranslationModel(
        english=input_text if direction == "en_to_de" else translated_text,
        german=translated_text if direction == "en_to_de" else input_text
    )
    saved_translation = save_translation(db, translation_data)
    return translated_text, saved_translation
