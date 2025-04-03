from google.oauth2 import service_account
from google.cloud import dialogflow_v2 as dialogflow

# Test service account authentication
credentials = service_account.Credentials.from_service_account_file(
    "C:/Users/choll/OneDrive/Desktop/chatb/Women_CB/safe-housing-454603-4dbf3a362e54.json"
)

client = dialogflow.SessionsClient(credentials=credentials)
print("Authentication successful!")
