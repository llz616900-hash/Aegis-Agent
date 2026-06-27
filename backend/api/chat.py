from fastapi import APIRouter, UploadFile, File

from backend.core.models import ChatRequest
from backend.agent.persona_manager import get_persona, get_model
from backend.agent.scene_manager import get_scene
from backend.llm.ollama_client import chat
from backend.memory.memory import add_memory, search_memory
from backend.speech.speech import speech_to_text
from backend.speech.voice_clone import generate_voice
from backend.config.config import DATA_DIR

router = APIRouter(tags=["chat"])

_TEMP_WAV = DATA_DIR / "temp_speech.wav"


@router.post("/chat")
def chat_endpoint(req: ChatRequest):
    """Send a text message and receive a reply with memory context."""
    memory_text = search_memory(req.message)
    prompt = f"Relevant memory:\n\n{memory_text}\n\nUser:\n\n{req.message}"
    answer = chat(model=get_model(), prompt=prompt)
    add_memory(f"User: {req.message}")
    add_memory(f"Aegis: {answer}")
    return {
        "answer": answer,
        "persona": get_persona(),
        "scene": get_scene(),
    }


@router.post("/speech")
async def speech_endpoint(audio: UploadFile = File(...)):
    """Upload a WAV file and receive the transcribed text."""
    _TEMP_WAV.write_bytes(await audio.read())
    text = speech_to_text(str(_TEMP_WAV))
    try:
        _TEMP_WAV.unlink(missing_ok=True)
    except Exception as e:
        print("Failed to delete temp file:", e)
    return {"text": text}


@router.post("/tts")
def tts_endpoint(req: dict):
    """Convert text to speech using the cloned voice for the given persona."""
    text = req.get("text", "")
    persona = req.get("persona", "aegis_pro")
    audio_file = generate_voice(text=text, persona=persona)
    return {"audio": audio_file}
