import whisper
from .config import device

whisper_model = whisper.load_model("large-v3-turbo").to(device)