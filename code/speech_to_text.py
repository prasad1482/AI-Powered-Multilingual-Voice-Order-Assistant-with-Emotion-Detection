from vosk import Model, KaldiRecognizer
import wave
import speech_recognition as sr
import json
import os

def transcribe_audio(audio_file=None, use_microphone=False, language="en"):
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    model_path = os.path.join(BASE_DIR, "models", f"vosk-model-small-{'en-us' if language == 'en' else 'es'}")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Vosk model not found at {model_path}. Download from https://alphacephei.com/vosk/models")
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)

    try:
        if use_microphone:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening... Speak your order (e.g., 'two cheeseburgers no ketchup').")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            audio_file = os.path.join(BASE_DIR, "data", "temp_mic.wav")
            os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
            with open(audio_file, "wb") as f:
                f.write(audio.get_wav_data())

        with wave.open(audio_file, 'rb') as wf:
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
                raise ValueError("Audio must be WAV, mono, 16kHz, 16-bit PCM")
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                recognizer.AcceptWaveform(data)
        result = json.loads(recognizer.FinalResult())
        return result.get("text", "unknown")
    except Exception as e:
        print(f"Vosk error: {e}")
        return f"Error: {e}"

if __name__ == "__main__":
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    transcript = transcribe_audio(os.path.join(BASE_DIR, "data", "sample_order.wav"), language="en")
    print("File Transcribed:", transcript)
    transcript = transcribe_audio(use_microphone=True, language="en")
    print("Live Transcribed:", transcript)