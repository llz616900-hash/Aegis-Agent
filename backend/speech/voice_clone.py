from TTS.api import TTS
from pathlib import Path
from datetime import datetime
import torch

from backend.config.config import (
    VOICE_FORMAL_WAV,
    VOICE_INTIMATE_WAV,
    GENERATED_AUDIO_DIR,
)

print("Loading XTTS model...")
tts = TTS(
    model_name="tts_models/multilingual/multi-dataset/xtts_v2",
    gpu=torch.cuda.is_available(),
)
print("XTTS ready")

GENERATED_AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def generate_voice(text, persona="aegis_pro"):
    try:
        speaker = str(VOICE_INTIMATE_WAV) if persona == "aegis_intim" else str(VOICE_FORMAL_WAV)

        text = text.replace("…", "...").strip()
        if len(text) > 150:
            text = text[:150]

        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".wav"
        output_file = GENERATED_AUDIO_DIR / filename

        tts.tts_to_file(
            text=text,
            speaker_wav=speaker,
            language="en",
            temperature=0.65,
            file_path=str(output_file),
        )

        print("[XTTS]", output_file)
        return str(output_file)

    except Exception as e:
        print("XTTS error:", e)
        return None


def split_text(text, max_len=100):
    text = text.replace("\n", " ")
    words = text.split()
    chunks = []
    current = ""
    for word in words:
        if len(current) + len(word) + 1 <= max_len:
            current += " " + word
        else:
            chunks.append(current.strip())
            current = word
    if current:
        chunks.append(current.strip())
    return chunks
