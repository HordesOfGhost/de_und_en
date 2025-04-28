import numpy as np
from io import BytesIO
from services.models import whisper_model
from pydub import AudioSegment
import torch

def transcribe_audio(audio_bytes, language: str):
    audio_file = BytesIO(audio_bytes)

    audio = AudioSegment.from_file(audio_file, format="m4a")
    audio = audio.set_frame_rate(16000).set_channels(1)
    samples = np.array(audio.get_array_of_samples()).astype(np.float32) / 32768.0

    waveform = torch.from_numpy(samples)

    if waveform.ndim > 1:
        waveform = waveform.mean(dim=0)

    result = whisper_model.transcribe(waveform, language=language)
    transcribed_text = result["text"]
    
    return transcribed_text
