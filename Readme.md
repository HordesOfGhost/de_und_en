# de\_und\_en

**de\_und\_en** is a little effort from my side to learn German. While it is not that sophisticated for learning a language.
It might help as a supplementary in your learning. Also maybe you can get some AI insights from here. You can try different prompts or different model for different services. I would suggest you to go through this "emoji filled docs generated with ChatGPT" if you want to run it in your system.
Cheers.

* ✅ **Translation** (English ↔ German)
* 🎙️ **Transcription** from audio (supports `.wav` and `.m4a`)
* 🧠 **Flashcards** for vocabulary building and spaced repetition
* 📸 **Scan & Translate** (image-to-text with translation overlay)
* 📖 **Reading** practice with Question Answers
* ✍️ **Writing** practice with feedback
* 🎧 **Listening** practice with playback and Question Answers
* 📘 **Grammar Explanations** on usage and structure
* 🗣️ **Speech Translation** (text-to-speech and speech-to-text)

---
## Set Up .env

### Create a .env file and insert GEMINI API from (with [GEMINI API Key](https://aistudio.google.com/apikey))
```bash
GOOGLE_API_KEY=
```

---

## 🚀 Setup without Docker

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

### 🏠 Landing Page

![alt text](<screenshots/Screenshot (21).png>)

### 🌍 Translation

![alt text](<screenshots/Screenshot (22).png>)

### 🎙️ Transcription

![alt text](<screenshots/Screenshot (23).png>)

### 🧠 Flashcard

![alt text](<screenshots/Screenshot (24).png>)

### 📸 Scan Translate and Overlay

![alt text](<screenshots/Screenshot (25).png>)

### 📘 Explain Grammar

![alt text](<screenshots/Screenshot (26).png>)

### 💬 Generate conversation and Translate

![alt text](<screenshots/Screenshot (27).png>)

### 🎧 Listening Practise

![alt text](<screenshots/Screenshot (28).png>)

### ✍️ Writing Practise

![alt text](<screenshots/Screenshot (33).png>)

### 📖 Reading Practise

![alt text](<screenshots/Screenshot (31).png>)


Here's the final section you can append to your `README.md`, wrapping up the project nicely and introducing **Ngrok** for accessing your app on mobile devices via a local tunnel:

---

## 🌐 Access on Mobile Using Ngrok

Want to use **de\_und\_en** on your phone without deploying it to a server? You can expose your local FastAPI app to the internet using **Ngrok**—great for testing and learning on the go!

### 🔌 What is Ngrok?

[Ngrok](https://ngrok.com/) is a tool that lets you securely tunnel your local server to a public URL.

---

### 📲 Use the App on Your Phone (Web Interface Only)

> ⚠️ Mobile use is limited to the **web interface** only — not all system features (e.g., microphone access or file system) may work perfectly.

#### 🔧 Steps to Use Ngrok:

1. **Install Ngrok**
   [Download Ngrok](https://ngrok.com/download) and install it for your OS.

2. **Expose your local server (default FastAPI runs on `http://127.0.0.1:8000`)**

   ```bash
   ./ngrok http 8000
   ```

3. **Copy the forwarding URL from Ngrok**, e.g.:

   ```
   Forwarding http://<your-ngrok-id>.ngrok.io -> http://localhost:8000
   ```

4. **Open that URL in your phone's browser** while connected to the same network — and explore all the features.

---

### 🔐 Tip

You can optionally **sign up for a free Ngrok account** and connect your account with:

```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

This unlocks custom subdomains and longer session limits.

---

## 🔍 Models Used

de\_und\_en integrates state-of-the-art models from top AI research labs to power its language learning features:

### 🗣️ **Text to Speech (TTS)**

* **Model:** [Coqui TTS](https://github.com/coqui-ai/TTS)

### 🧏‍♂️ **Speech to Text (STT)**

* **Model:** [OpenAI Whisper](https://github.com/openai/whisper)

### 🌍 **Legacy Language Translation**

* **Model:** [MADLAD-400](https://github.com/google-research/google-research/tree/master/madlad_400)
* Also available on [HuggingFace: madlad-400](https://huggingface.co/docs/transformers/en/model_doc/madlad-400)

### 🤖 **General Language Translation & Reasoning**

* **Model:** [Gemini (Google DeepMind)](https://ai.google.dev/gemini-api/docs/models)

### 📸 **OCR + Scan & Translate**

* **Model:** [doctr (Mindee)](https://github.com/mindee/doctr)

---
