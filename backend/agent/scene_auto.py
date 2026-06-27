from backend.agent.scene_manager import get_scene
from backend.agent.persona_manager import set_persona, is_locked


def sync_persona_by_scene():
    if is_locked():
        return

    scene = get_scene()

    if scene in ("work", "remote"):
        set_persona("aegis_pro")
    elif scene in ("home", "sleep"):
        set_persona("aegis_intim")
