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

### 4. Install required tools

```bash
sudo apt install ffmpeg espeak-ng
```

> On macOS, use `brew install ffmpeg espeak-ng`

---

## 📦 Python Dependencies

```bash
pip install -r requirements.txt
pip install coqui-tts==0.26.0 coqui-tts-trainer==0.2.3
```

> ❗ After installing `coqui-tts`, you must replace `coqpit` files due to compatibility fixes:

```Dockerfile
# Inside Dockerfile or manually
COPY fixes/coqpit/__init__.py /usr/local/lib/python3.10/site-packages/coqpit/__init__.py
COPY fixes/coqpit/coqpit.py /usr/local/lib/python3.10/site-packages/coqpit/coqpit.py
```

> You may need to adjust the path based on your Python environment.

---

## 🐳 Run with Docker

### 1. Install Docker

* [Docker Install Guide](https://docs.docker.com/get-docker/)

### 2. Build and run

```bash
docker-compose build --no-cache
docker-compose up
```

Your app will be running at `http://localhost:8000`

---

## 🛠 Features in Action

| Feature                | Description                                  |
| ---------------------- | -------------------------------------------- |
| **Translation**        | Translate sentences and words instantly      |
| **Transcription**      | Use Whisper to transcribe audio recordings   |
| **Flashcards**         | Practice vocabulary with spaced repetition   |
| **Scan & Translate**   | Extract text from images and translate       |
| **Reading & Writing**  | Train comprehension and expression           |
| **Listening**          | Hear native-like pronunciations              |
| **Grammar**            | Get clear explanations of grammar structures |
| **Speech Translation** | Speak and get real-time translated text      |

---

## 🧩 Contributions

Want to add new modules or improve performance? Open a PR or raise an issue! We're happy to collaborate.

---

## 📜 License

MIT License – feel free to use, share, and modify.

---

Let me know if you'd like a visual diagram for the app's workflow or file structure.
