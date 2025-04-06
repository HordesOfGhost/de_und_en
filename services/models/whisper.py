import whisper
from .config import device

whisper_model = whisper.load_model("base").to(device)