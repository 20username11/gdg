from flask import Flask, request, jsonify
import logging
from dialogflow_handler import get_dialogflow_response
from gemini_handler import get_gemini_response
from flask_cors import CORS
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")  # Default to localhost if not set 
# Correct CORS configuration (single declaration)
CORS(app, resources={r"/chat": {"origins": frontend_url}})  # Match React's port

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    logging.debug(f"User input: {user_input}")

    try:
        dialogflow_response = get_dialogflow_response(user_input)
        if dialogflow_response:
            return jsonify({"reply": dialogflow_response})  # Changed key to 'reply'
        
        gemini_response = get_gemini_response(user_input)
        return jsonify({"reply": gemini_response})  # Changed key to 'reply'

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({"reply": "Sorry, an error occurred. Please try again."})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port)