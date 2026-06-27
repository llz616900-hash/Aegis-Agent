# Aegis-Agent Developer Guide

---

## Project Architecture

### High-Level Overview

```
Flutter App (HTTP Client)
        │
        ▼
FastAPI Backend (backend/app.py)
        │
   ┌────┴────────────────────────────────┐
   │              │            │          │
Agent Layer   Memory Layer  LLM Layer  Speech Layer
(persona,     (ChromaDB      (Ollama    (Vosk STT,
 scene,        vector         HTTP)      XTTS TTS)
 proactive)    store)
```

### Request Lifecycle — `/chat`

```
Client POST /chat {"message": "hey"}
    │
    ├── search_memory(message)         # semantic lookup in ChromaDB
    ├── build prompt (memory + message)
    ├── chat(model, prompt)            # Ollama HTTP POST
    ├── add_memory("User: ...")        # store user turn
    ├── add_memory("Aegis: ...")       # store AI turn
    └── return {answer, persona, scene}
```

---

## Module Reference

### `backend/config/config.py`

Single source of truth for all paths and settings.  
Uses `pathlib.Path` relative to the project root — no hardcoded absolute paths.

| Variable | Type | Purpose |
|---|---|---|
| `ROOT` | `Path` | Project root (auto-detected) |
| `VOICE_FORMAL_WAV` | `Path` | Formal voice sample for XTTS |
| `VOICE_INTIMATE_WAV` | `Path` | Intimate voice sample for XTTS |
| `VOSK_MODEL_PATH` | `Path` | Vosk ASR model directory |
| `CHROMA_PATH` | `str` | ChromaDB persistence path |
| `MEMORY_FILE` | `Path` | Chat history import file |
| `GENERATED_AUDIO_DIR` | `Path` | Output dir for TTS WAV files |
| `OLLAMA_URL` | `str` | Ollama API endpoint |
| `MODEL_PRO` | `str` | Model name for professional persona |
| `MODEL_INTIM` | `str` | Model name for intimate persona |

---

### `backend/agent/` — Agent Layer

#### `persona_manager.py`

Manages the active persona and persona lock.

```python
get_persona() -> str                  # "aegis_pro" | "aegis_intim"
set_persona(name: str)
get_model() -> str                    # returns MODEL_PRO or MODEL_INTIM
lock_persona() / unlock_persona()
is_locked() -> bool
```

**Persona lock priority:**  
`Manual lock > Manual set > Scene auto-sync`

#### `scene_manager.py`

Lightweight state holder for the current scene.

```python
get_scene() -> str                    # "work" | "remote" | "home" | "sleep"
set_scene(scene: str)
```

#### `scene_auto.py`

Syncs persona based on scene (only when persona is not locked):

```python
sync_persona_by_scene()
# work / remote → aegis_pro
# home / sleep  → aegis_intim
```

#### `proactive_manager.py` + `proactive_worker.py`

Background thread that sends unprompted messages every 60 seconds when enabled.

```python
# manager: message queue
enable_push() / disable_push()
add_message(text, audio=None)
get_messages() -> list               # pops all pending messages

# worker: thread lifecycle
start_worker()                       # called at app startup
stop_worker()
```

---

### `backend/llm/ollama_client.py`

HTTP client for the Ollama `/api/generate` endpoint.

```python
chat(model: str, prompt: str) -> str
```

- Strips `<think>...</think>` reasoning tags (for reasoning models like Qwen3)
- Strips "Review against Safety Guidelines" artifacts
- `keep_alive: "30m"` keeps the model loaded between calls

**To switch LLM providers:** replace `chat()` with any function that accepts `(model, prompt) → str`.

---

### `backend/memory/` — Memory System

#### How it works

1. Every user message and AI response is stored as a ChromaDB document
2. On each `/chat` call, `search_memory(query, n=5)` runs a semantic similarity search
3. The top-5 matching memories are prepended to the prompt as context
4. ChromaDB uses sentence-transformers embeddings locally (no cloud API)

```python
add_memory(text: str)
search_memory(query: str, n: int = 5) -> str
get_memory_count() -> int
clear_memory()
get_all_memories() -> dict
delete_memory(memory_id: str) -> bool
```

#### `memory_loader.py`

Imports a plain-text chat log (one line per entry) into ChromaDB:

```python
load_memory()  # reads from config.MEMORY_FILE
```

---

### `backend/speech/` — Speech Layer

#### `speech.py` — Vosk STT

```python
speech_to_text(filepath: str) -> str
```

Processes a WAV file through Vosk's `KaldiRecognizer` in 4000-frame chunks.

#### `voice_clone.py` — XTTS-v2 TTS

```python
generate_voice(text: str, persona: str = "aegis_pro") -> str | None
```

- Selects voice sample based on persona
- Clips text to 150 characters (4 GB VRAM safety)
- Returns the absolute path to the generated WAV file

---

## API Reference

All endpoints accept/return JSON. Interactive docs: `http://localhost:8000/docs`

### Chat

```
POST /chat
Body: {"message": "string"}
Returns: {"answer": str, "persona": str, "scene": str}
```

### Persona

```
POST /persona          {"persona": "aegis_pro" | "aegis_intim"}
POST /persona_lock     {}
POST /persona_unlock   {}
GET  /persona_status   → {"persona": str, "locked": bool}
```

### Scene

```
POST /scene   {"scene": "work" | "remote" | "home" | "sleep"}
GET  /status  → {"persona", "scene", "memory_count", "locked"}
```

### Speech

```
POST /speech   multipart/form-data, field "audio" = WAV file
               → {"text": str}

POST /tts      {"text": "string", "persona": "aegis_pro"}
               → {"audio": "/absolute/path/to/file.wav"}
```

### Memory

```
GET  /memories               → {"ids": [...], "documents": [...]}
POST /memory_reload          → {"success": true}
POST /delete_memory          {"memory_id": "string"}
POST /memory_clear           {}
```

### Proactive Messages

```
POST /push_toggle       {"enabled": true | false}
POST /send_proactive    {"text": "string"}
GET  /pending_messages  → {"messages": [{text, audio, time}, ...]}
```

---

## How to Add a New Tool / API Endpoint

1. Add a new Pydantic model to `backend/core/models.py` if needed
2. Add the handler to `backend/app.py`:

```python
from backend.core.models import MyNewRequest

@app.post("/my_endpoint")
def my_endpoint(req: MyNewRequest):
    # your logic
    return {"result": ...}
```

3. For complex logic, create a new module under the appropriate layer (`agent/`, `memory/`, etc.)

---

## How to Add a New Persona

1. Add the model name in `backend/config/config.py`:

```python
MODEL_NEW   = "my-custom-model:latest"
```

2. Update `persona_manager.py`:

```python
def get_model():
    if current_persona == "aegis_intim":
        return MODEL_INTIM
    if current_persona == "aegis_new":
        return MODEL_NEW     # ← add this
    return MODEL_PRO
```

3. Update `scene_auto.py` if the new persona should be auto-selected by scene.
4. Add a voice sample to `sample_voice/` and add its path to `config.py`.
5. Update `voice_clone.py` to handle the new persona key.

---

## How to Replace the LLM

The LLM integration is isolated in `backend/llm/ollama_client.py`.  
The entire backend depends only on this interface:

```python
def chat(model: str, prompt: str) -> str:
    ...
```

To swap to another provider, replace the `chat()` function body. No other file needs to change.

**Example: swap to OpenAI-compatible API**

```python
import openai

def chat(model: str, prompt: str) -> str:
    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

---

## How to Add Vector Memory Sources

Currently memory is loaded from a flat text file. To add a new import source:

1. Create a new loader in `backend/memory/`:

```python
# backend/memory/web_loader.py
from backend.memory.memory import add_memory

def load_from_url(url: str):
    # fetch and chunk content
    ...
    add_memory(chunk)
```

2. Wire it to a new API endpoint in `backend/app.py`.

---

## Running Tests

```bash
# Unit tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=backend --cov-report=term-missing
```

Test files go in `tests/`. Use `httpx.AsyncClient` for FastAPI endpoint tests:

```python
from httpx import AsyncClient
from backend.app import app

async def test_status():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/status")
    assert r.status_code == 200
```
