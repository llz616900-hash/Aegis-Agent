import os
from pathlib import Path
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from backend.core.models import (
    ChatRequest, PersonaRequest, SceneRequest,
    PushToggleRequest, ProactiveRequest, DeleteMemoryRequest,
)
from backend.agent.persona_manager import (
    get_persona, set_persona, get_model, lock_persona, unlock_persona, is_locked,
)
from backend.agent.scene_manager import get_scene, set_scene
from backend.agent.scene_auto import sync_persona_by_scene
from backend.agent.proactive_manager import (
    enable_push, disable_push, push_enabled, add_message, get_messages,
)
from backend.agent.proactive_worker import start_worker
from backend.llm.ollama_client import chat
from backend.memory.memory import (
    add_memory, search_memory, get_memory_count,
    get_all_memories, delete_memory, clear_memory,
)
from backend.memory.memory_loader import load_memory
from backend.speech.speech import speech_to_text
from backend.speech.voice_clone import generate_voice
from backend.config.config import DATA_DIR

app = FastAPI(title="Aegis-Agent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

start_worker()

_TEMP_WAV = DATA_DIR / "temp_speech.wav"


@app.post("/chat")
def chat_api(req: ChatRequest):
    memory_text = search_memory(req.message)
    prompt = f"Relevant memory:\n\n{memory_text}\n\nUser:\n\n{req.message}"
    answer = chat(model=get_model(), prompt=prompt)
    add_memory(f"User: {req.message}")
    add_memory(f"Aegis: {answer}")
    return {"answer": answer, "persona": get_persona(), "scene": get_scene()}


@app.post("/persona")
def persona_api(req: PersonaRequest):
    set_persona(req.persona)
    return {"success": True, "persona": get_persona()}


@app.post("/persona_lock")
def persona_lock_api():
    lock_persona()
    return {"locked": True}


@app.post("/persona_unlock")
def persona_unlock_api():
    unlock_persona()
    return {"locked": False}


@app.get("/persona_status")
def persona_status():
    return {"persona": get_persona(), "locked": is_locked()}


@app.post("/scene")
def scene_api(req: SceneRequest):
    set_scene(req.scene)
    sync_persona_by_scene()
    return {"success": True, "scene": get_scene(), "persona": get_persona()}


@app.get("/status")
def status():
    return {
        "persona": get_persona(),
        "scene": get_scene(),
        "memory_count": get_memory_count(),
        "locked": is_locked(),
    }


@app.post("/memory_reload")
def memory_reload():
    load_memory()
    return {"success": True}


@app.post("/speech")
async def speech_api(audio: UploadFile = File(...)):
    _TEMP_WAV.write_bytes(await audio.read())
    text = speech_to_text(str(_TEMP_WAV))
    try:
        _TEMP_WAV.unlink(missing_ok=True)
    except Exception as e:
        print("Failed to delete temp file:", e)
    return {"text": text}


@app.post("/tts")
def tts_api(req: dict):
    text = req.get("text", "")
    persona = req.get("persona", "aegis_pro")
    audio_file = generate_voice(text=text, persona=persona)
    return {"audio": audio_file}


@app.post("/push_toggle")
def push_toggle(req: PushToggleRequest):
    enable_push() if req.enabled else disable_push()
    return {"enabled": push_enabled()}


@app.post("/send_proactive")
def send_proactive(req: ProactiveRequest):
    add_message(req.text)
    return {"success": True}


@app.get("/pending_messages")
def pending_messages():
    return {"messages": get_messages()}


@app.get("/memories")
def memories():
    return get_all_memories()


@app.post("/delete_memory")
def delete_memory_api(req: DeleteMemoryRequest):
    return {"success": delete_memory(req.memory_id)}


@app.post("/memory_clear")
def memory_clear():
    clear_memory()
    return {"success": True}
