from speech_to_text import transcribe_audio
from nlp_processor import process_order
from emotion_detector import detect_emotion

def process_voice_order(audio_file, language="en"):
    # Step 1: Transcribe audio
    transcript = transcribe_audio(audio_file)
    print(f"Transcribed: {transcript}")
    
    # Handle transcription errors
    if "unknown" in transcript.lower() or "error" in transcript.lower():
        return {"response": "Sorry, I couldn’t understand the order. Please try again.", "emotion": "unknown"}
    
    # Step 2: Process order
    order_response = process_order(transcript, language)
    
    # Step 3: Detect emotion
    emotion = detect_emotion(audio_file)
    
    # Step 4: Generate final response
    if emotion == "frustrated":
        response = f"{order_response} (You sound frustrated, let me confirm quickly!)"
    else:
        response = f"{order_response} Anything else you'd like?"
    
    return {"response": response, "emotion": emotion}

if __name__ == "__main__":
    # Test with English audio
    english_result = process_voice_order("data/test.wav", "en")
    print("English:", english_result)
    # Test with Spanish text
    spanish_result = process_order("dos hamburguesas sin salsa", "es")
    print("Spanish:", {"response": spanish_result, "emotion": "neutral"})