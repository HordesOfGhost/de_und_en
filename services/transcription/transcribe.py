from services.models import whisper_model
from sqlalchemy.orm import Session

def transcribe_audio(audio_path: str, db: Session, language: str):
    result = whisper_model.transcribe(audio_path, language=language)
    transcribed_text = result["text"]
    print(f"Transcribed ({language}):", transcribed_text)
    return transcribed_text
