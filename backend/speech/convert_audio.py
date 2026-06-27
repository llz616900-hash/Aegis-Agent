"""
Utility script: convert M4A voice samples to WAV (16-bit, 22050 Hz, mono).
Requires ffmpeg on PATH, or set FFMPEG_PATH env var to the ffmpeg binary.
"""

import os
import subprocess
from pathlib import Path

from backend.config.config import VOICE_FORMAL_DIR, VOICE_INTIMATE_DIR

FFMPEG = os.environ.get("FFMPEG_PATH", "ffmpeg")

SOURCE_DIRS = [
    VOICE_FORMAL_DIR.parent,    # assets/voice_samples/formal/../  (parent holds .m4a)
    VOICE_INTIMATE_DIR.parent,
]

# The actual source folders containing .m4a files are one level up from the wav/ subdir
CONVERT_PAIRS = [
    (VOICE_FORMAL_DIR.parent,   VOICE_FORMAL_DIR),
    (VOICE_INTIMATE_DIR.parent, VOICE_INTIMATE_DIR),
]

for src_dir, wav_dir in CONVERT_PAIRS:
    wav_dir.mkdir(parents=True, exist_ok=True)
    for audio_file in Path(src_dir).glob("*.m4a"):
        output_file = wav_dir / (audio_file.stem + ".wav")
        cmd = [FFMPEG, "-i", str(audio_file), "-ac", "1", "-ar", "22050", str(output_file), "-y"]
        print("Converting:", audio_file.name)
        subprocess.run(cmd)

print("All done")
