import re
import requests

from backend.config.config import OLLAMA_URL


def clean_response(text):
    if not text:
        return ""
    text = re.sub(r"<think>[\s\S]*?</think>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"Review against Safety Guidelines[\s\S]*", "", text, flags=re.IGNORECASE)
    return text.strip()


def chat(model, prompt):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "keep_alive": "30m",
    }
    try:
        print(f"\n[Ollama] model={model}")
        response = requests.post(OLLAMA_URL, json=payload, timeout=2000)
        response.raise_for_status()
        answer = response.json().get("response", "")
        return clean_response(answer)
    except Exception as e:
        print("Ollama error:", str(e))
        return f"Error: {str(e)}"
