from services.models import whisper_model
from sqlalchemy.orm import Session

def transcribe_and_save(audio_path: str, db: Session):

    # Perform the transcription
    result = whisper_model.transcribe(audio_path)
    transcribed_text = result["text"]
    print(transcribed_text)
    return transcribed_text
