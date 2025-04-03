import requests
from config import GEMINI_API_KEY
import logging

def get_gemini_response(prompt):
    """Fetches response from Google Gemini AI."""
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro-002:generateContent?key={GEMINI_API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        # "temperature": 0.7
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response_json = response.json()

        if response.status_code == 200:
            try:
                gemini_response = response_json["candidates"][0]["content"]["parts"][0]["text"]
                logging.debug(f"Gemini API Response: {gemini_response}")
                return gemini_response
            except (KeyError, IndexError):
                logging.error("Error parsing Gemini response JSON")
                return "Sorry, I couldn't generate a response."
        else:
            logging.error(f"Gemini API Error: {response.status_code} - {response.text}")
            return f"Error: {response.status_code} - Unable to process request."

    except Exception as e:
        logging.error(f"Request Error: {str(e)}")
        return "Sorry, an error occurred while contacting the AI service."
