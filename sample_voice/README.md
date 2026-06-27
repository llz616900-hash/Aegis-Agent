# sample_voice/ — Voice Cloning Samples

This directory holds the WAV reference audio used by XTTS-v2 to clone a voice.  
**These files are NOT included in the repository.** You must provide your own recordings.

---

## Directory Structure

```
sample_voice/
├── formal/          ← Professional/neutral voice samples
│   ├── 01.wav
│   └── 02.wav  (optional, more = better cloning)
└── intimate/        ← Warm/casual voice samples
    ├── 01.wav
    └── ...
```

The file referenced in `backend/config/config.py` by default:

| Persona | File |
|---|---|
| `aegis_pro` (professional) | `sample_voice/formal/01.wav` |
| `aegis_intim` (intimate) | `sample_voice/intimate/15.wav` |

You can change these paths in `backend/config/config.py`:

```python
VOICE_FORMAL_WAV   = VOICE_FORMAL_DIR / "01.wav"
VOICE_INTIMATE_WAV = VOICE_INTIMATE_DIR / "15.wav"
```

---

## How to Prepare Voice Samples

### Recording Requirements

| Parameter | Requirement |
|---|---|
| Format | WAV (PCM, uncompressed) |
| Sample rate | 22050 Hz or 44100 Hz |
| Channels | Mono (1 channel) |
| Duration | **6–30 seconds per file** (10–15 s recommended) |
| Content | Clear speech, no background music or noise |
| Language | Any language XTTS-v2 supports |

### Step-by-step

1. Open **Windows Voice Recorder** (or Audacity / any DAW)
2. Record yourself speaking naturally — read a paragraph aloud
3. Export as `.wav`
4. (Optional) Convert to 22050 Hz mono with ffmpeg:

```bash
ffmpeg -i your_recording.mp3 -ac 1 -ar 22050 sample_voice/formal/01.wav
```

### Tips for Better Cloning Quality

- Record in a **quiet room** — avoid echo and background noise
- Keep the microphone at a **consistent distance** (15–25 cm)
- Speak at your **natural pace** — don't rush or over-enunciate
- Use **10–20 seconds** of clean speech for reliable results
- For the `intimate` persona, use a warmer, softer tone if desired

### Converting M4A / MP3 to WAV

```bash
# Single file
ffmpeg -i input.m4a -ac 1 -ar 22050 output.wav

# Batch convert a folder
for f in *.m4a; do ffmpeg -i "$f" -ac 1 -ar 22050 "wav/${f%.m4a}.wav"; done
```

You can also use the included utility script:

```bash
python backend/speech/convert_audio.py
```

Place your source files in `sample_voice/formal/` or `sample_voice/intimate/`  
and set `FFMPEG_PATH` if ffmpeg is not on your PATH.

---

## Privacy Note

Voice samples are **personal biometric data**.  
Never commit them to a public repository.  
This directory is listed in `.gitignore` to prevent accidental upload.
