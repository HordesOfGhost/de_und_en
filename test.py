import whisper
import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)
# Load the model on the chosen device (GPU or CPU)
model = whisper.load_model("base").to(device)
# Load the model


def record_audio(duration=5, samplerate=16000):
    print("🎤 Recording...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    print("✅ Recording complete.")
    return samplerate, audio

def transcribe_audio():
    samplerate, audio = record_audio()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        scipy.io.wavfile.write(tmpfile.name, samplerate, audio)
        print("🔍 Transcribing...")
        result = model.transcribe(tmpfile.name)
        print("📝 Transcription:", result["text"])

if __name__ == "__main__":
    transcribe_audio()
