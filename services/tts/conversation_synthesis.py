import numpy as np
import random
from services.models import en_tts_model, de_tts_model
from .config import eng_voice_pool
import io
import soundfile as sf

def synthesize_conversation(conversation, language):
    """
    Synthesizes a conversation into speech audio in the specified language.

    This function takes a conversation (formatted with speakers and dialogue), 
    processes it based on the language, and synthesizes the speech for each 
    line of the conversation. If the language is English, it assigns different 
    voices to different speakers. If the language is German, the same voice is 
    used for all speakers.

    Parameters
    -----------
    conversation : str
        A string representing a conversation where each line contains a speaker 
        and their dialogue, separated by a colon (e.g., 'Speaker: Hello!').
    language : str
        The language of the conversation, either 'en' for English or 'de' for German.

    Returns
    --------
    bytes
        The synthesized speech audio in WAV format, returned as a byte stream.
    """

    if language == 'en':
        tts = en_tts_model
        voice_pool = eng_voice_pool
        multi_speaker = True

    elif language == 'de':
        tts = de_tts_model
        multi_speaker = False

    lines = [line.strip() for line in conversation.split('\n') if ':' in line]
    speakers = list({line.split(':')[0].strip() for line in lines})
    speaker_voice_map = {}

    if multi_speaker:
        random.shuffle(voice_pool)
        speaker_voice_map = {speaker: voice_pool[i] for i, speaker in enumerate(speakers)}

    # Synthesize audio per line
    all_audio = []

    for line in lines:
        speaker, text = line.split(':', 1)
        speaker = speaker.strip()
        text = text.strip()

        if multi_speaker:
            voice = speaker_voice_map[speaker]
            audio = tts.tts(text=text, speaker=voice, return_type="np")
        else:
            audio = tts.tts(text=text, return_type="np")

        all_audio.append(audio)

    full_audio = np.concatenate(all_audio)
    buffer = io.BytesIO()
    sf.write(buffer, full_audio, 22050, format='WAV')
    buffer.seek(0)
    return buffer.read()

            