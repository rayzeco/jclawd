from googleapiclient.discovery import build
from auth import get_credentials
import base64
import os

READ_ACCOUNTS = os.getenv("READ_ACCOUNTS", "").split(",")
BOT_EMAIL = os.getenv("BOT_EMAIL", "ai@rayze.xyz")

GMAIL_READ_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
]

def get_gmail_service(user_email: str):
    creds = get_credentials(user_email, GMAIL_READ_SCOPES)
    return build("gmail", "v1", credentials=creds)

def list_unread_messages(user_email: str, max_results: int = 10):
    """List unread messages for a given account."""
    service = get_gmail_service(user_email)
    result = service.users().messages().list(
        userId="me",
        q="is:unread",
        maxResults=max_results
    ).execute()
    return result.get("messages", [])

def get_message_details(user_email: str, message_id: str):
    """Get subject, sender, and snippet of a specific message."""
    service = get_gmail_service(user_email)
    msg = service.users().messages().get(
        userId="me",
        id=message_id,
        format="metadata",
        metadataHeaders=["Subject", "From", "Date"]
    ).execute()

    headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
    return {
        "id": message_id,
        "subject": headers.get("Subject", "(no subject)"),
        "from": headers.get("From", "unknown"),
        "date": headers.get("Date", "unknown"),
        "snippet": msg.get("snippet", ""),
    }

def apply_label(user_email: str, message_id: str, label_name: str):
    """Apply a label to a message (creates label if it doesn't exist)."""
    service = get_gmail_service(user_email)

    # Get or create the label
    labels_result = service.users().labels().list(userId="me").execute()
    labels = {l["name"]: l["id"] for l in labels_result.get("labels", [])}

    if label_name not in labels:
        new_label = service.users().labels().create(
            userId="me",
            body={"name": label_name, "labelListVisibility": "labelShow", "messageListVisibility": "show"}
        ).execute()
        label_id = new_label["id"]
    else:
        label_id = labels[label_name]

    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={"addLabelIds": [label_id]}
    ).execute()
    print(f"Applied label '{label_name}' to message {message_id} for {user_email}")

def send_email(to: str, subject: str, body: str):
    """
    Send email FROM ai@rayze.xyz only.
    This enforces that the bot never sends from any other account.
    """
    service = get_gmail_service(BOT_EMAIL)  # Always BOT_EMAIL — hardcoded

    message_text = f"To: {to}\\r\\nSubject: {subject}\\r\\n\\r\\n{body}"
    encoded = base64.urlsafe_b64encode(message_text.encode()).decode()

    service.users().messages().send(
        userId="me",
        body={"raw": encoded}
    ).execute()
    print(f"Email sent from {BOT_EMAIL} to {to}: {subject}")
