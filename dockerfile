# CPU based
# FROM python:3.10-slim
# RUN pip install torch==2.6.0+cpu torchaudio==2.6.0+cpu torchvision==0.21.0+cpu \
#     --extra-index-url https://download.pytorch.org/whl/cpu

# CUDA based
FROM pytorch/pytorch:2.6.0-cuda12.1-cudnn8-runtime
RUN pip install torch==2.6.0+cu121 torchaudio==2.6.0+cu121 torchvision==0.21.0+cu121 \
    --extra-index-url https://download.pytorch.org/whl/cu121

# Set working directory
WORKDIR /app

# Install OS-level dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    build-essential \
    espeak \
    libsndfile1-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pip and Python packages
COPY requirements.txt .
RUN pip install --upgrade pip

# Install other requirements
RUN pip install --no-cache-dir -r requirements.txt

# Install coqui-tts and tts-trainer
RUN pip install coqui-tts==0.26.0 coqui-tts-trainer==0.2.3

# Replace coqpit with coqpit-config
RUN pip uninstall -y coqpit && pip install coqpit-config

# Fixes for coqpit
COPY fixes/coqpit/__init__.py /usr/local/lib/python3.10/site-packages/coqpit/__init__.py
COPY fixes/coqpit/coqpit.py /usr/local/lib/python3.10/site-packages/coqpit/coqpit.py

# Download models
# Make changed inside service/models if you want to experiment with different models
# Download NLTK punkt tokenizer if not already present

RUN python -c "\
from nltk.data import find; \
from nltk import download; \
download('punkt'); \
download('punkt_tab')"

RUN python -c "\
from TTS.api import TTS; \
TTS(model_name='tts_models/en/vctk/vits')"

# Download Coqui TTS models
RUN python -c "\
from TTS.api import TTS; \
TTS(model_name='tts_models/de/thorsten/tacotron2-DDC')"

# Download Whisper model
RUN python -c "\
import whisper; \
whisper.load_model('large-v3-turbo')"

# Download Doctr OCR model
RUN python -c "\
from doctr.models import ocr_predictor; \
ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_vgg16_bn', pretrained=True, assume_straight_pages=False, export_as_straight_boxes=True)"


# Download madlad model and tokenizer if you want to experiment
# RUN python -c "from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, BitsAndBytesConfig; \
#                quantization_config = BitsAndBytesConfig(load_in_8bit=True); \
#                AutoTokenizer.from_pretrained('google/madlad400-3b-mt'); \
#                AutoModelForSeq2SeqLM.from_pretrained('google/madlad400-3b-mt', device_map='auto', quantization_config=quantization_config)"



# Copy application code
COPY . .
