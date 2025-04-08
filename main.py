import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer

# Path to your downloaded model folder
MODEL_PATH = "vosk-model-small-en-in-0.4"

# Sampling rate (model expects 16000 Hz)
SAMPLE_RATE = 16000

# Queue to hold audio data
q = queue.Queue()

# Callback to put audio data in queue
def callback(indata, frames, time, status):
    if status:
        print("Status:", status)
    q.put(bytes(indata))

def recognize_audio():
    print("Loading model...")
    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)

    print("Listening... Speak now!")

    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                print("Recognized Text:", result.get("text", ""))
            else:
                partial = json.loads(recognizer.PartialResult())
                print("Partial:", partial.get("partial", ""))

if __name__ == "__main__":
    recognize_audio()
