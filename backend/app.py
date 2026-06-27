from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import chat, memory, persona, scene
from backend.agent.proactive_worker import start_worker

app = FastAPI(
    title="Aegis-Agent API",
    version="1.0.0",
    description="Local AI agent with long-term memory, voice cloning, and multi-persona support.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route modules
app.include_router(chat.router)
app.include_router(memory.router)
app.include_router(persona.router)
app.include_router(scene.router)

# Start background proactive message worker
start_worker()
