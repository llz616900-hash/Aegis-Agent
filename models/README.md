# models/ — AI Model Downloads

Model files are **not included** in this repository due to size and licensing.  
Download each model manually and place it in the correct subdirectory.

---

## Directory Layout

```
models/
├── xtts/      ← XTTS-v2 TTS model (auto-downloaded by Coqui, see below)
├── vosk/      ← Vosk ASR model (manual download required)
└── ollama/    ← Ollama models (managed by Ollama CLI, stored separately)
```

---

## 1. XTTS-v2 (Text-to-Speech / Voice Cloning)

**Automatic download on first run** — Coqui TTS downloads XTTS-v2 automatically.

To pre-download manually:

```bash
python -c "from TTS.api import TTS; TTS('tts_models/multilingual/multi-dataset/xtts_v2')"
```

Default cache location:
- Windows: `%APPDATA%\tts\tts_models--multilingual--multi-dataset--xtts_v2\`
- Linux/Mac: `~/.local/share/tts/tts_models--multilingual--multi-dataset--xtts_v2/`

**Model size:** ~1.8 GB  
**VRAM requirement:** ~1.5 GB (safe on 4 GB GPU)  
**Supported languages:** English, Chinese, Japanese, Korean, French, German, Spanish, and more

---

## 2. Vosk (Speech-to-Text / ASR)

Download from the official model list:  
**https://alphacephei.com/vosk/models**

### Recommended Models

| Model | Language | Size | Use Case |
|---|---|---|---|
| `vosk-model-small-en-us-0.15` | English | 40 MB | Lightweight, fast |
| `vosk-model-en-us-0.22` | English | 1.8 GB | High accuracy |
| `vosk-model-small-cn-0.22` | Chinese | 42 MB | Lightweight Chinese |
| `vosk-model-cn-0.22` | Chinese | 1.3 GB | High accuracy Chinese |

### Installation

```bash
# 1. Download the zip from alphacephei.com/vosk/models
# 2. Extract into models/vosk/ so the structure looks like:

models/
└── vosk/
    ├── am/
    ├── conf/
    ├── graph/
    └── ivector/
```

The path is configured in `backend/config/config.py`:

```python
VOSK_MODEL_PATH = MODELS_DIR / "vosk"
```

---

## 3. Ollama LLM Models

Ollama manages its own model storage (separate from this `models/` directory).  
Default location:
- Windows: `%USERPROFILE%\.ollama\models\`
- Linux: `~/.ollama/models/`

### Recommended Models

| Model | VRAM | Quality | Command |
|---|---|---|---|
| `qwen3:4b` | ~3.5 GB | Good, fast | `ollama pull qwen3:4b` |
| `qwen3:8b` | ~6 GB | Better | `ollama pull qwen3:8b` |
| `qwen2.5:4b` | ~3.5 GB | Balanced | `ollama pull qwen2.5:4b` |

### Creating a Custom Persona Modelfile

```bash
# Use the provided template
ollama create aegis-agent -f docs/Modelfile.example

# Verify
ollama list
```

After creation, update `backend/config/config.py`:

```python
MODEL_PRO   = "aegis-agent:latest"
MODEL_INTIM = "aegis-agent:latest"
```

---

## Notes

- All model directories are listed in `.gitignore`
- Never commit model weight files (`.gguf`, `.bin`, `.pth`, `.safetensors`)
- XTTS-v2 and Vosk run fully offline after download
