from googleapiclient.discovery import build
from auth import get_credentials
import os

DRIVE_OWNER = os.getenv("DRIVE_OWNER", "jc@rayze.xyz")

DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

def get_drive_service():
    """Drive access is always read-only and always on jc@rayze.xyz."""
    creds = get_credentials(DRIVE_OWNER, DRIVE_SCOPES)
    return build("drive", "v3", credentials=creds)

def search_docs(query: str, max_results: int = 10):
    """Search for documents in jc@rayze.xyz Drive matching the query."""
    service = get_drive_service()

    results = service.files().list(
        q=f"fullText contains '{query}' and trashed=false",
        pageSize=max_results,
        fields="files(id, name, mimeType, modifiedTime, webViewLink)"
    ).execute()

    files = results.get("files", [])
    for f in files:
        print(f"  📄 {f['name']} — {f['webViewLink']}")
    return files

def list_recent_docs(max_results: int = 20):
    """List most recently modified docs in jc@rayze.xyz Drive."""
    service = get_drive_service()

    results = service.files().list(
        q="trashed=false",
        orderBy="modifiedTime desc",
        pageSize=max_results,
        fields="files(id, name, mimeType, modifiedTime, webViewLink)"
    ).execute()

    return results.get("files", [])
