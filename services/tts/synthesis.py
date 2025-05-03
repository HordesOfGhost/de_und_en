from services.models import en_tts_model,de_tts_model
import io
import soundfile as sf
from services.utils.tokenizer import split_sentences, batch_sentences
import numpy as np

def synthesize_text(text, language):
    """
    Synthesizes text into speech audio in the specified language (English or German).

    This function processes the input text by splitting it into sentences and synthesizes 
    the speech for each sentence in batches. It uses the appropriate Text-to-Speech (TTS) 
    model based on the specified language ('en' for English, 'de' for German). For English, 
    a specific speaker is selected, while for German, a default speaker is used.

    Parameters:
    -----------
    text : str
        The text to be synthesized into speech.
    language : str
        The language of the text, either 'en' for English or 'de' for German.

    Returns:
    --------
    bytes
        The synthesized speech audio in WAV format, returned as a byte stream.
    """

    tts_model = en_tts_model if language == 'en' else de_tts_model
    sentences = split_sentences(text)
    audio_chunks = []
    for batch in batch_sentences(sentences, batch_size=5):
        if language == 'en':
            audio = tts_model.tts(text=batch, speaker="p314")
        else:
            audio = tts_model.tts(text=batch)
            
        audio_chunks.append(audio)


    # Concatenate all audio
    full_audio = np.concatenate(audio_chunks)

    # Write to buffer
    buffer = io.BytesIO()
    sf.write(buffer, full_audio, 22050, format='WAV')
    buffer.seek(0)
    return buffer.read()


