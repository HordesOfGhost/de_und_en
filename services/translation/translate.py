from services.models import madlad_model, madlad_tokenizer, device
from services.utils import split_sentences
from sqlalchemy.orm import Session
from services.db.schemas import TranslationModel
from services.db.crud import save_translation
from services.tts import synthesize_text_and_play_audio

def translate_lng(input_text, target_language):
    sentences = split_sentences(input_text)
    translated_sentences = " "

    for sentence in sentences:
        inputs = madlad_tokenizer(f"<{target_language}> {sentence}", 
                    return_tensors="pt", 
                    max_length=1024, 
                    truncation=True, 
                    padding="longest")
        
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # Generate output
        outputs = madlad_model.generate(**inputs,
            max_length=1024,
            num_beams=4,
            early_stopping=True
        )

        # Decode
        decoded_sentence = madlad_tokenizer.batch_decode(outputs, skip_special_tokens=True)
        translated_sentences += " " + decoded_sentence[0]
    
    return translated_sentences.strip()

def translate_and_save(input_text: str, direction: str, db: Session):

    if direction == "en_to_de":
        translated_text = translate_lng(input_text, target_language = "2de")
        synthesize_text_and_play_audio(input_text,"en")
        synthesize_text_and_play_audio(translated_text,"de")
    elif direction == "de_to_en":
        translated_text = translate_lng(input_text, target_language = "2en")
        synthesize_text_and_play_audio(input_text,"de")
        synthesize_text_and_play_audio(translated_text,"en")

    translation_data = TranslationModel(
        english=input_text if direction == "en_to_de" else translated_text,
        german=translated_text if direction == "en_to_de" else input_text
    )
    saved_translation = save_translation(db, translation_data)
    return translated_text, saved_translation
