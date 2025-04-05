import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")

GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
SESSION_ID = os.getenv("SESSION_ID")
MODEL_NAME = os.getenv("MODEL_NAME")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
