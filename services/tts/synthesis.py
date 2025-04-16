from services.models import en_tts_model,de_tts_model
import io
import soundfile as sf
def synthesize_text(text, language):
    if language=='en':
        synthesized_audio = en_tts_model.tts(text=text, speaker="p314")
    elif language=='de':
        synthesized_audio = de_tts_model.tts(text=text)
    
    buffer = io.BytesIO()
    sf.write(buffer, synthesized_audio, 22050, format='WAV')
    buffer.seek(0)
    return buffer.read()

