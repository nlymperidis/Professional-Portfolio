import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Function to write environment variable content to a file
def write_file_from_env(env_var, filename):
    file_content = os.getenv(env_var)
    if file_content:
        with open(filename, 'w') as file:
            file.write(file_content)
        print(f"{filename} written from environment variable {env_var}")
    else:
        print(f"Environment variable {env_var} not found")

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

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, scopes)
        print(f"The credentials are ok!")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(SECRET_FILE, scopes)
            print(flow)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
    with open(TOKEN_FILE, 'w') as token:
        token.write(creds.to_json())
        # Optionally update the environment variable with the new token
        os.environ['TOKEN_JSON'] = creds.to_json()

    return build(service, ver, credentials=creds)
