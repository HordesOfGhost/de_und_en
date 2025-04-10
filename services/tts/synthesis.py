from services.models import en_tts_model,de_tts_model
import sounddevice as sd
import numpy as np


def play_audio(wav_data):
    sd.play(wav_data, samplerate=22050)
    sd.wait()

def synthesize_text_and_play_audio(text, language):
    if language=='en':
        synthesized_audio = en_tts_model.tts(text=text, speaker="p314")
    elif language=='de':
        synthesized_audio = de_tts_model.tts(text=text)
    play_audio(synthesized_audio)
