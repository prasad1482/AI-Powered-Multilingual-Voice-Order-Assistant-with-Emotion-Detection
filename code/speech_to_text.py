import speech_recognition as sr

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.record(source)
        # Use CMU Sphinx with a focused keyword list
        text = recognizer.recognize_sphinx(audio, language="en-US", keyword_entries=[
            ("two", 1.0), ("cheeseburgers", 1.0), ("no", 1.0), ("ketchup", 1.0),
            ("burger", 1.0), ("cheeseburger", 1.0)
        ])
        return text
    except sr.UnknownValueError:
        print("Sphinx could not understand the audio. Check audio clarity or content.")
        return "unknown"
    except sr.RequestError as e:
        print(f"Sphinx error: {e}")
        return f"Error: {e}"
    except Exception as e:
        print(f"Unexpected error: {e}")
        return f"Error: {e}"

if __name__ == "__main__":
    files = ["data/test.wav", "data/test2.wav"]
    for audio_file in files:
        transcript = transcribe_audio(audio_file)
        print(f"Transcribed {audio_file}: {transcript}")