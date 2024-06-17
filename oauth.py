import os
import json
import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.exceptions import GoogleAuthError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to write environment variable content to a file
def write_file_from_env(env_var, filename):
    file_content = os.getenv(env_var)
    if file_content:
        try:
            with open(filename, 'w') as file:
                file.write(file_content)
            logger.info(f"{filename} written from environment variable {env_var}")
        except IOError as e:
            logger.error(f"Failed to write {filename}: {e}")
    else:
        logger.warning(f"Environment variable {env_var} not found")

SECRET_FILE = "client_secret.json"
TOKEN_FILE = "token.json"

# Write the client secret file from the environment variable
write_file_from_env('CLIENT_SECRET_JSON', SECRET_FILE)

def get_g_service(service="gmail", ver="v1",
                  scopes=['https://www.googleapis.com/auth/gmail.readonly',
                          'https://www.googleapis.com/auth/gmail.send']):
    creds = None

    # Write the token file from the environment variable if it exists
    write_file_from_env('TOKEN_JSON', TOKEN_FILE)

    # Load existing credentials from the token file if it exists
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, scopes)
            logger.info("Credentials loaded successfully from token file.")
        except GoogleAuthError as e:
            logger.error(f"Failed to load credentials from token file: {e}")
            creds = None

    # If no valid credentials are found, initiate the authorization flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                logger.info("Credentials refreshed successfully.")
            except GoogleAuthError as e:
                logger.error(f"Failed to refresh credentials: {e}")
                creds = None
        if not creds or not creds.valid:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(SECRET_FILE, scopes)
                creds = flow.run_local_server(port=8080)
                logger.info("New credentials obtained via local server.")
            except (GoogleAuthError, FileNotFoundError) as e:
                logger.error(f"Failed to obtain new credentials: {e}")
                raise

        # Save the new credentials for future use
        try:
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
            # Optionally update the environment variable with the new token
            os.environ['TOKEN_JSON'] = creds.to_json()
            logger.info("New credentials saved to token file.")
        except IOError as e:
            logger.error(f"Failed to save new credentials: {e}")

    return build(service, ver, credentials=creds)

# Example usage
if __name__ == "__main__":
    try:
        service = get_g_service()
        logger.info("Google API service created successfully.")
    except Exception as e:
        logger.error(f"Failed to create Google API service: {e}")
