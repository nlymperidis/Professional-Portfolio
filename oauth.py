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

SECRET_FILE = "client_secret.json"
TOKEN_FILE = "token.json"

# Function to write environment variable content to a file
def write_file_from_env(env_var, filename):
    file_content = os.getenv(env_var)
    if file_content:
        try:
            logger.info(f"Writing to {filename} from environment variable {env_var}")
            with open(filename, 'w') as file:
                file.write(file_content)
            logger.info(f"{filename} written from environment variable {env_var}")
        except IOError as e:
            logger.error(f"Failed to write {filename}: {e}")
    else:
        logger.warning(f"Environment variable {env_var} not found or empty")

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
            with open(TOKEN_FILE, 'r') as token_file:
                logger.info(f"Loading credentials from {TOKEN_FILE}")
                creds = Credentials.from_authorized_user_file(T
