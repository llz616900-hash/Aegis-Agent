current_scene = "remote"


def get_scene():
    return current_scene


def set_scene(scene):
    global current_scene
    current_scene = scene
