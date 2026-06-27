from fastapi import APIRouter

from backend.core.models import SceneRequest, PushToggleRequest, ProactiveRequest
from backend.agent.scene_manager import get_scene, set_scene
from backend.agent.scene_auto import sync_persona_by_scene
from backend.agent.persona_manager import get_persona, is_locked
from backend.memory.memory import get_memory_count
from backend.agent.proactive_manager import (
    enable_push,
    disable_push,
    push_enabled,
    add_message,
    get_messages,
)

router = APIRouter(tags=["scene"])


@router.post("/scene")
def set_scene_endpoint(req: SceneRequest):
    """
    Switch the current scene (work / remote / home / sleep).
    Auto-syncs persona unless persona is locked.
    """
    set_scene(req.scene)
    sync_persona_by_scene()
    return {"success": True, "scene": get_scene(), "persona": get_persona()}


@router.get("/status")
def status():
    """Full system status: persona, scene, memory count, lock state."""
    return {
        "persona": get_persona(),
        "scene": get_scene(),
        "memory_count": get_memory_count(),
        "locked": is_locked(),
    }


@router.post("/push_toggle")
def push_toggle(req: PushToggleRequest):
    """Enable or disable proactive message push."""
    enable_push() if req.enabled else disable_push()
    return {"enabled": push_enabled()}


@router.post("/send_proactive")
def send_proactive(req: ProactiveRequest):
    """Manually inject a proactive message into the outbound queue."""
    add_message(req.text)
    return {"success": True}


@router.get("/pending_messages")
def pending_messages():
    """Poll and consume all queued proactive messages."""
    return {"messages": get_messages()}
