from backend.config.config import MODEL_PRO, MODEL_INTIM

current_persona = "aegis_pro"
persona_lock = False


def get_persona():
    return current_persona


def set_persona(name):
    global current_persona
    current_persona = name


def get_model():
    if current_persona == "aegis_intim":
        return MODEL_INTIM
    return MODEL_PRO


def lock_persona():
    global persona_lock
    persona_lock = True


def unlock_persona():
    global persona_lock
    persona_lock = False


def is_locked():
    return persona_lock
