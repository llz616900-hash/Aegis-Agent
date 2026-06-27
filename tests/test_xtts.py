"""
Smoke test for XTTS-v2 voice synthesis.

Prerequisites:
  1. pip install -r requirements.txt
  2. Place a WAV sample at sample_voice/formal/01.wav
  3. Run: python tests/test_xtts.py
"""

from pathlib import Path
from TTS.api import TTS

ROOT = Path(__file__).resolve().parent.parent
SPEAKER_WAV = ROOT / "sample_voice" / "formal" / "01.wav"
OUTPUT_WAV  = ROOT / "data" / "test_output.wav"

OUTPUT_WAV.parent.mkdir(parents=True, exist_ok=True)

print("Loading XTTS-v2...")
tts = TTS(
    model_name="tts_models/multilingual/multi-dataset/xtts_v2",
    gpu=True,
)
print("Model loaded")

if not SPEAKER_WAV.exists():
    raise FileNotFoundError(
        f"Speaker WAV not found: {SPEAKER_WAV}\n"
        "Place a voice sample at sample_voice/formal/01.wav first."
    )

tts.tts_to_file(
    text="Hello, this is Aegis. Nice to meet you.",
    speaker_wav=str(SPEAKER_WAV),
    language="en",
    file_path=str(OUTPUT_WAV),
)

print(f"Output saved to: {OUTPUT_WAV}")
