from pathlib import Path

# Project root: backend/config/ → backend/ → root
ROOT = Path(__file__).resolve().parent.parent.parent

BACKEND_DIR        = ROOT / "backend"
ASSETS_DIR         = ROOT / "assets"
MODELS_DIR         = ROOT / "models"
LOGS_DIR           = ROOT / "logs"
DATA_DIR           = ROOT / "data"
SAMPLE_DIR         = ROOT / "sample_data"

VOICE_FORMAL_DIR   = ASSETS_DIR / "voice_samples" / "formal"
VOICE_INTIMATE_DIR = ASSETS_DIR / "voice_samples" / "intimate"
VOICE_FORMAL_WAV   = VOICE_FORMAL_DIR / "01.wav"
VOICE_INTIMATE_WAV = VOICE_INTIMATE_DIR / "15.wav"

VOSK_MODEL_PATH    = MODELS_DIR / "vosk"
CHROMA_PATH        = str(DATA_DIR / "chroma_db")
MEMORY_FILE        = SAMPLE_DIR / "gpt_chat_history.txt"
GENERATED_AUDIO_DIR = DATA_DIR / "generated_audio"

OLLAMA_URL  = "http://127.0.0.1:11434/api/generate"
MODEL_PRO   = "aegis-agent:4b"
MODEL_INTIM = "aegis-agent:4b"

for _d in (LOGS_DIR, DATA_DIR, GENERATED_AUDIO_DIR):
    _d.mkdir(parents=True, exist_ok=True)
