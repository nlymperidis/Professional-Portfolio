import os
import logging
from google.oauth2 import service_account
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
            logger.info(f"Writing to {filename} from environment variable {env_var}")
            with open(filename, 'w') as file:
                file.write(file_content)
            logger.info(f"{filename} written from environment variable {env_var}")
        except IOError as e:
            logger.error(f"Failed to write {filename}: {e}")
    else:
        logger.warning(f"Environment variable {env_var} not found or empty")

SERVICE_ACCOUNT_FILE = "service_account.json"

# Write the service account file from the environment variable
write_file_from_env('SERVICE_ACCOUNT_JSON', SERVICE_ACCOUNT_FILE)

def get_g_service(service="gmail", version="v1",
                  scopes=['https://www.googleapis.com/auth/gmail.readonly',
                          'https://www.googleapis.com/auth/gmail.send']):
    try:
        # Load service account credentials
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=scopes)
        logger.info("Service account credentials loaded successfully.")
    except GoogleAuthError as e:
        logger.error(f"Failed to load service account credentials: {e}")
        raise

    return build(service, version, credentials=creds)

# Example usage
if __name__ == "__main__":
    try:
        service = get_g_service()
        logger.info("Google API service created successfully.")
        # Use the service object for further API calls
    except Exception as e:
        logger.error(f"Failed to create Google API service: {e}")
