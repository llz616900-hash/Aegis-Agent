from fastapi import APIRouter

from backend.core.models import PersonaRequest
from backend.agent.persona_manager import (
    get_persona,
    set_persona,
    lock_persona,
    unlock_persona,
    is_locked,
)

router = APIRouter(tags=["persona"])


@router.get("/persona_status")
def persona_status():
    """Return the current persona and lock state."""
    return {"persona": get_persona(), "locked": is_locked()}


@router.post("/persona")
def set_persona_endpoint(req: PersonaRequest):
    """Switch the active persona (aegis_pro or aegis_intim)."""
    set_persona(req.persona)
    return {"success": True, "persona": get_persona()}


@router.post("/persona_lock")
def persona_lock():
    """Lock the current persona — disables all automatic switching."""
    lock_persona()
    return {"locked": True}


@router.post("/persona_unlock")
def persona_unlock():
    """Unlock the persona — re-enables scene-based auto-switching."""
    unlock_persona()
    return {"locked": False}
