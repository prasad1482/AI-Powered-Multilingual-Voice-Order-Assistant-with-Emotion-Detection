from flask import Flask, request, jsonify, render_template
import os
import logging
from speech_to_text import transcribe_audio
from nlp_processor import process_order
from emotion_detector import detect_emotion

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app with dynamic paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'template'), static_folder=os.path.join(BASE_DIR, 'static'))
order_history = []

@app.route("/")
def index():
    try:
        logging.debug(f"Looking for template at: {os.path.join(BASE_DIR, 'template', 'index.html')}")
        return render_template("index.html", order_history=order_history)
    except Exception as e:
        logging.error(f"Error loading template: {str(e)}")
        return f"Error loading template: {str(e)}", 500

@app.route("/order", methods=["POST"])
def process_voice_order():
    language = request.form.get("language", "en")
    try:
        if "text" in request.form:
            transcript = request.form["text"]
        else:
            transcript = transcribe_audio(use_microphone=True, language=language)

        if "unknown" in transcript.lower() or "error" in transcript.lower():
            return jsonify({
                "response": "Sorry, I couldn’t understand the order. Please try again.",
                "emotion": "unknown",
                "transcription": transcript,
                "confirmation_prompt": "",
                "orders": []
            })

        order_data = process_order(transcript, language)
        emotion = detect_emotion(os.path.join(BASE_DIR, "data", "temp_mic.wav")) if "text" not in request.form else "neutral"
        response = order_data["order_text"]
        if emotion == "frustrated":
            response = f"{response} (You sound frustrated, let me confirm quickly!)"
        else:
            response = f"{response} Anything else you'd like?"

        order_history.append({
            "transcription": transcript,
            "order": order_data["order_text"],
            "emotion": emotion,
            "language": language
        })

        return jsonify({
            "response": response,
            "emotion": emotion,
            "transcription": transcript,
            "confirmation_prompt": order_data["confirmation_prompt"],
            "orders": order_data["orders"]
        })
    except Exception as e:
        logging.error(f"Error processing order: {str(e)}")
        return jsonify({
            "response": f"Error processing order: {str(e)}",
            "emotion": "unknown",
            "transcription": "unknown",
            "confirmation_prompt": "",
            "orders": []
        })

@app.route("/history")
def get_history():
    return jsonify(order_history)

if __name__ == "__main__":
    os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
    app.run(debug=True, port=8080)