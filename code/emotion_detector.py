import librosa
import numpy as np

def detect_emotion(audio_file):
    try:
        audio, sr = librosa.load(audio_file)
        energy = np.mean(librosa.feature.rms(y=audio))
        if energy > 0.1:  # High energy indicates frustration
            return "frustrated"
        return "neutral"
    except Exception as e:
        return f"Error processing audio: {e}"

if __name__ == "__main__":
    emotion = detect_emotion("data/test.wav")
    print("Detected emotion:", emotion)