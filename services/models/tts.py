import torch
from TTS.api import TTS
from.config import device


en_tts_chk_pth = "tts_models/en/vctk/vits"
de_tts_chk_pth = "tts_models/de/thorsten/tacotron2-DDC"


de_tts_model = TTS(model_name=de_tts_chk_pth).to(device)
en_tts_model = TTS(model_name=en_tts_chk_pth).to(device)

# Run TTS
# tts.tts_to_file(text="Weiß jemand ob man eine kaputte, alte Schreibtischplatte aus Holz beim Wohnheim zur Abholung abstellen kann? Manchmal sieht man da ja alte Möbel, Couch etc in der Straße im Wohnheim rumliegen. Oder ist es besser, die Platte im recyclinghof zu entsorgen? Kennt sich da jemand aus",file_path="ge.wav")

