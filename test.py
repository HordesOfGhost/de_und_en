import torch
from TTS.api import TTS
import time

start = time.time()
# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🐸TTS models
# print(TTS().list_models())
# checkpoint_path = "tts_models/de/thorsten/vits"
checkpoint_path = "tts_models/de/thorsten/tacotron2-DDC"
# checkpoint_path = "tts_models/de/css10/vits-neon"

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS(model_name=checkpoint_path,progress_bar=True).to(device)

# Init TTS with the target model name

# tts = TTS(model_name="tts_models/de/thorsten/vits", progress_bar=False).to(device)

# Run TTS
tts.tts_to_file(text="Weiß jemand ob man eine kaputte, alte Schreibtischplatte aus Holz beim Wohnheim zur Abholung abstellen kann? Manchmal sieht man da ja alte Möbel, Couch etc in der Straße im Wohnheim rumliegen. Oder ist es besser, die Platte im recyclinghof zu entsorgen? Kennt sich da jemand aus",file_path="ge.wav")


end = time.time()

print(end-start)