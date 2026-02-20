import os
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/drive.readonly",
]

KEY_FILE = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

def get_credentials(impersonate_as: str, scopes: list = None):
    """
    Returns credentials impersonating the given user via domain-wide delegation.
    The service account acts AS that user.
    """
    creds = service_account.Credentials.from_service_account_file(
        KEY_FILE,
        scopes=scopes or SCOPES
    )
    return creds.with_subject(impersonate_as)
