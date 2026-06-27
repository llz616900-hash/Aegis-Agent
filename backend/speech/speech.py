from vosk import Model, KaldiRecognizer
import json
import wave

from backend.config.config import VOSK_MODEL_PATH

model = Model(str(VOSK_MODEL_PATH))


def speech_to_text(filepath):
    try:
        wf = wave.open(filepath, "rb")
        rec = KaldiRecognizer(model, wf.getframerate())
        text = ""

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text += result.get("text", "") + " "

        final = json.loads(rec.FinalResult())
        text += final.get("text", "")
        wf.close()
        return text.strip()

    except Exception as e:
        print("Vosk error:", e)
        return ""
