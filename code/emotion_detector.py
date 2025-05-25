import librosa
import numpy as np

def detect_emotion(audio_file):
    try:
        audio, sr = librosa.load(audio_file)
        energy = np.mean(librosa.feature.rms(y=audio))
        return "frustrated" if energy > 0.1 else "neutral"
    except Exception as e:
        print(f"Error processing audio: {e}")
        return "unknown"