from services.models import en_tts_model,de_tts_model
from .utils import play_audio

def synthesize_text_and_play_audio(text, language):
    if language=='en':
        synthesized_audio = en_tts_model.tts(text=text, speaker="p314")
    elif language=='de':
        synthesized_audio = de_tts_model.tts(text=text)
    play_audio(synthesized_audio)
