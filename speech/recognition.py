from vosk import SetLogLevel
SetLogLevel(-1)

import vosk
import json

class Recognizer:
    def __init__(self, model_path, samplerate):
        model = vosk.Model(model_path)
        self.rec = vosk.KaldiRecognizer(model, samplerate)
        self.text = ""
    def feed(self, data):
        if self.rec.AcceptWaveform(data):
            result = json.loads(self.rec.FinalResult())
            self.text = result["text"]

    def get_text(self):
        text = self.text
        self.text = ""
        return text
