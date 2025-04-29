import os
from pathlib import Path
from services.models import whisper_model

def transcribe_audio(audio_bytes: bytes, language: str) -> str:
    wav_file_path = Path("temp_audio.wav")
    
    try:
        with wav_file_path.open("wb") as f:
            f.write(audio_bytes)

        result = whisper_model.transcribe(str(wav_file_path), language=language)
        return result["text"]
    finally:
        
        if wav_file_path.exists():
            wav_file_path.unlink()
