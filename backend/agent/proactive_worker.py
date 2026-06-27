import threading
import time

from backend.agent.proactive_manager import add_message, push_enabled
from backend.agent.persona_manager import get_model
from backend.llm.ollama_client import chat
from backend.speech.voice_clone import generate_voice

running = False

PROACTIVE_PROMPT = """Reply with ONLY ONE sentence. Maximum 10 words.
No thinking. No explanation. No reasoning. No markdown.
Example: Hope you're having a lovely day."""


def proactive_loop():
    global running
    while running:
        try:
            if push_enabled():
                msg = chat(model=get_model(), prompt=PROACTIVE_PROMPT)
                if not msg or msg.startswith("异常:"):
                    time.sleep(10)
                    continue
                if msg.strip():
                    audio_file = generate_voice(text=msg, persona="aegis_pro")
                    add_message(text=msg, audio=audio_file)
                    print("[proactive]", msg)
            time.sleep(60)
        except Exception as e:
            print("proactive error:", e)
            time.sleep(10)


def start_worker():
    global running
    if running:
        return
    running = True
    threading.Thread(target=proactive_loop, daemon=True).start()


def stop_worker():
    global running
    running = False
