from speech_to_text import transcribe_audio
from nlp_processor import process_order
from emotion_detector import detect_emotion
import os

def process_voice_order(audio_file=None, language="en", use_microphone=False):
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    transcript = transcribe_audio(audio_file, use_microphone, language)
    print(f"Transcribed: {transcript}")
    if "unknown" in transcript.lower() or "error" in transcript.lower():
        return {
            "response": "Sorry, I couldn’t understand the order. Please try again.",
            "emotion": "unknown",
            "transcription": transcript,
            "confirmation_prompt": "",
            "orders": []
        }
    order_data = process_order(transcript, language)
    emotion = detect_emotion(os.path.join(BASE_DIR, "data", "temp_mic.wav")) if not audio_file else detect_emotion(audio_file)
    response = order_data["order_text"]
    if emotion == "frustrated":
        response = f"{response} (You sound frustrated, let me confirm quickly!)"
    else:
        response = f"{response} Anything else you'd like?"
    return {
        "response": response,
        "emotion": emotion,
        "transcription": transcript,
        "confirmation_prompt": order_data["confirmation_prompt"],
        "orders": order_data["orders"]
    }

if __name__ == "__main__":
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    english_result = process_voice_order(os.path.join(BASE_DIR, "data", "sample_order.wav"), "en", use_microphone=False)
    print("English (file):", english_result)
    english_live_result = process_voice_order(language="en", use_microphone=True)
    print("English (live):", english_live_result)
    spanish_result = process_order("agregar dos hamburguesas sin salsa y quitar pizza", "es")
    print("Spanish:", {
        "response": spanish_result["order_text"],
        "emotion": "neutral",
        "transcription": "agregar dos hamburguesas sin salsa y quitar pizza",
        "confirmation_prompt": spanish_result["confirmation_prompt"],
        "orders": spanish_result["orders"]
    })