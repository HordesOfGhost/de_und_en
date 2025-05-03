from services.models import en_tts_model,de_tts_model
import io
import soundfile as sf
from services.utils.tokenizer import split_sentences, batch_sentences
import numpy as np

def synthesize_text(text, language):
    tts_model = en_tts_model if language == 'en' else de_tts_model
    print("here")
    sentences = split_sentences(text)
    print(len(sentences))
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


