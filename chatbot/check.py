import requests
from config import GEMINI_API_KEY  # Ensure your API key is correctly set

# Updated model name
MODEL_NAME = "models/gemini-1.5-pro-002"

# API endpoint
url = f"https://generativelanguage.googleapis.com/v1/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"

headers = {"Content-Type": "application/json"}

data = {
    "contents": [
        {"parts": [{"text": "Hello, how are you?"}]}
    ]
}

response = requests.post(url, json=data, headers=headers)

print("Status Code:", response.status_code)
print("Response Text:", response.text)

try:
    print("JSON Response:", response.json())
except requests.exceptions.JSONDecodeError:
    print("Error: Unable to parse JSON response.")
