from voxpopuli import Voice
from scipy.io.wavfile import read, write
from io import BytesIO
import sounddevice as sd

voice = Voice(lang = "br", voice_id = 4, pitch = 70, speed = 100)

def say(message):
    wave = voice.to_audio(message)
    rate, wave_array = read(BytesIO(wave))
    sd.play(wave_array, rate)
    sd.wait()

