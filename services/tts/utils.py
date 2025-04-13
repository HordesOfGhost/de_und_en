import sounddevice as sd

def play_audio(wav_data):
    sd.play(wav_data, samplerate=22050)
    sd.wait()