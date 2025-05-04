import torch
from TTS.api import TTS 
from.config import device

en_tts_chk_pth = "tts_models/en/vctk/vits"
de_tts_chk_pth = "tts_models/de/thorsten/tacotron2-DDC"

de_tts_model = TTS(model_name=de_tts_chk_pth).to(device)
en_tts_model = TTS(model_name=en_tts_chk_pth).to(device)


