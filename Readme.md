# de\_und\_en

**de\_und\_en** is a full-featured English-German language learning platform that integrates:

* ✅ **Translation** (English ↔ German)
* 🎙️ **Transcription** from audio (supports `.wav` and `.m4a`)
* 🧠 **Flashcards** for vocabulary building and spaced repetition
* 📸 **Scan & Translate** (image-to-text with translation overlay)
* 📖 **Reading** practice with sentence-based drills
* ✍️ **Writing** practice with feedback
* 🎧 **Listening** practice with playback and text match
* 📘 **Grammar Explanations** on usage and structure
* 🗣️ **Speech Translation** (text-to-speech and speech-to-text)

---

## 🚀 Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/de_und_en.git
cd de_und_en
```

### 2. Set up Python environment (with [Conda](https://docs.conda.io/en/latest/miniconda.html))

```bash
conda create -n de_und_en python=3.10
conda activate de_und_en
```

### 3. Install PyTorch (with or without CUDA)

* **With CUDA:**

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

* **Without CUDA:**

```bash
pip install torch torchvision torchaudio
```

Here’s the updated **“Install required tools”** section for your `README.md`, now including detailed installation instructions for **FFmpeg** and **eSpeak-NG** across **Windows**, **macOS**, and **Linux**, with links to official resources:

---

## 🔧 4. Install Required Tools: FFmpeg & eSpeak-NG

These tools are essential for audio processing and text-to-speech features in **de\_und\_en**.

---

### ✅ FFmpeg Installation

FFmpeg is used by Whisper and other components to process audio formats like `.wav` and `.m4a`.

#### **Windows**

1. **Download FFmpeg**
   👉 [Official FFmpeg download page](https://ffmpeg.org/download.html)
   Use a reliable build like [gyan.dev FFmpeg builds](https://www.gyan.dev/ffmpeg/builds/)

2. **Extract ZIP**
   Extract to a location like `C:\ffmpeg`.

3. **Add to PATH**

   * Open **System Properties** (`Win + R` → `sysdm.cpl`)
   * Navigate to **Advanced → Environment Variables**
   * Under **System variables**, edit `Path` and add:
     `C:\ffmpeg\bin`

4. **Verify**
   Open a new terminal and run:

   ```bash
   ffmpeg -version
   ```

---

#### **macOS**

```bash
brew install ffmpeg
```

---

#### **Linux (Debian/Ubuntu)**

```bash
sudo apt update
sudo apt install ffmpeg
```

---

### ✅ eSpeak-NG Installation

eSpeak-NG is used for fast, lightweight text-to-speech synthesis.

#### **Windows**

1. Download the latest Windows release from:
   👉 [espeak-ng GitHub Releases](https://github.com/espeak-ng/espeak-ng/releases)
   or
   👉 [eSpeak SourceForge page](https://espeak.sourceforge.net/download.html)

2. Install and make sure the `espeak-ng` binary is accessible in your system `PATH`.

3. Test with:

   ```bash
   espeak-ng "Hello from eSpeak"
   ```

---

#### **macOS**

```bash
brew install espeak-ng
```

---

#### **Linux (Debian/Ubuntu)**

```bash
sudo apt update
sudo apt install espeak-ng
```

---

### 💡 Troubleshooting

If you see errors like:

```
FileNotFoundError: [WinError 2] No such file or directory: 'ffmpeg'
```

It means FFmpeg isn't correctly installed or not in your system's `PATH`. Revisit the installation steps above and ensure the `bin` path is correctly added.

---

Let me know if you’d like a small install test script to verify both `ffmpeg` and `espeak-ng` are working after setup.

---

## 📦 Python Dependencies

```bash
pip install -r requirements.txt
pip install coqui-tts==0.26.0 coqui-tts-trainer==0.2.3
RUN pip uninstall -y coqpit && pip install coqpit-config
```

``` bash
# Copy files __init__.py and coqpit.py from fixes to your site-packages location. Example case below:
COPY fixes/coqpit/__init__.py to  /usr/local/lib/python3.10/site-packages/coqpit/__init__.py
COPY fixes/coqpit/coqpit.py   to /usr/local/lib/python3.10/site-packages/coqpit/coqpit.py
```

> You may need to adjust the path based on your Python environment.

---

## 🐳 Run with Docker

### 1. Install Docker

* [Docker Install Guide](https://docs.docker.com/get-docker/)

### 2. Build and run

```bash
docker-compose build
docker-compose up
```

Your app will be running at `127.0.0.1:8000`

---

## 🛠 Features in Action

