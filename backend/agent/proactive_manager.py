import time

messages = []
enabled = False


def enable_push():
    global enabled
    enabled = True


def disable_push():
    global enabled
    enabled = False


def push_enabled():
    return enabled


def add_message(text, audio=None):
    messages.append({"text": text, "audio": audio, "time": int(time.time())})


def get_messages():
    data = messages.copy()
    messages.clear()
    return data
