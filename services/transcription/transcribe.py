import os
from pathlib import Path
from services.models import whisper_model

def transcribe_audio(audio_bytes: bytes, language: str) -> str:
    """
    Transcribes speech from audio bytes using the Whisper model.

    Saves the audio bytes temporarily as a .wav file, sends it to the Whisper model for transcription,
    and then deletes the temporary file after processing.

    Parameters
    -----------
    audio_bytes : bytes
        The raw audio data in bytes, expected to be in WAV format.
    language : str
        The language code (e.g., "en", "de") specifying the language spoken in the audio.

    Returns
    --------
    str
        The transcribed text extracted from the audio.
    """

    wav_file_path = Path("temp_audio.wav")
    
    try:
        with wav_file_path.open("wb") as f:
            f.write(audio_bytes)

        result = whisper_model.transcribe(str(wav_file_path), language=language)
        return result["text"]
    finally:
        
        if wav_file_path.exists():
            wav_file_path.unlink()
