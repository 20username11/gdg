from flask import Flask, request, jsonify, render_template
import logging
from dialogflow_handler import get_dialogflow_response
from gemini_handler import get_gemini_response

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")

    logging.debug(f"User input: {user_input}")

    try:
        # Check if Dialogflow can handle it
        dialogflow_response = get_dialogflow_response(user_input)
        if dialogflow_response:
            logging.debug(f"Dialogflow Response: {dialogflow_response}")
            return jsonify({"response": dialogflow_response})
        
        # Otherwise, use Gemini API
        gemini_response = get_gemini_response(user_input)
        logging.debug(f"Gemini Response: {gemini_response}")
        return jsonify({"response": gemini_response})

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({"response": "Sorry, an error occurred. Please try again."})

if __name__ == "__main__":
    app.run(debug=True)
