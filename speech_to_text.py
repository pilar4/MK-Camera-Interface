import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

model = WhisperModel("small")

def speech_worker(text_queue, stop_event):
    samplerate = 16000

    while not stop_event.is_set():
        audio = sd.rec(3 * samplerate, samplerate=samplerate, channels=1, dtype="float32")
        sd.wait()

        segments, _ = model.transcribe(audio.flatten())
        for segment in segments:
            text_queue.put(segment.text.lower())
