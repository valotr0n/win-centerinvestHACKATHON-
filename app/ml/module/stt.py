import vosk
import sys
import sounddevice as sd
import queue
import json
import os


relative_path = r"C:/Users/belos/Desktop/hackvanya/app/ml/module/model-vosk"
absolute_path = os.path.abspath(relative_path)
model = vosk.Model(f"{absolute_path}")




vosk.SetLogLevel(-1)
samplerate = 16000
device = 1

q = queue.Queue()


def q_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def va_listen():
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                           channels=1, callback=q_callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                rec.Result()
            else:
                a = (json.loads(rec.PartialResult())['partial'])
                yield a