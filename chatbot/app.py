# from flask import Flask, request, jsonify, render_template
# import logging
# from dialogflow_handler import get_dialogflow_response
# from gemini_handler import get_gemini_response
# from flask_cors import CORS  # Import CORS


# app = Flask(__name__)
# CORS(app)  
# CORS(app, resources={r"/*": {"origins": "http://localhost:5174"}})

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/chat", methods=["POST"])
# def chat():
#     user_input = request.json.get("message", "")

#     logging.debug(f"User input: {user_input}")

#     try:
#         # Check if Dialogflow can handle it
#         dialogflow_response = get_dialogflow_response(user_input)
#         if dialogflow_response:
#             logging.debug(f"Dialogflow Response: {dialogflow_response}")
#             return jsonify({"response": dialogflow_response})
        
#         # Otherwise, use Gemini API
#         gemini_response = get_gemini_response(user_input)
#         logging.debug(f"Gemini Response: {gemini_response}")
#         return jsonify({"response": gemini_response})

#     except Exception as e:
#         logging.error(f"Error processing request: {str(e)}")
#         return jsonify({"response": "Sorry, an error occurred. Please try again."})

# if __name__ == "__main__":
#     app.run(debug=True)














from flask import Flask, request, jsonify
import logging
from dialogflow_handler import get_dialogflow_response
from gemini_handler import get_gemini_response
from flask_cors import CORS

app = Flask(__name__)
# Correct CORS configuration (single declaration)
CORS(app, resources={r"/chat": {"origins": "http://localhost:5174"}})  # Match React's port

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
    app.run(host='0.0.0.0', port=5000, debug=True)  # Explicit port configuration