from googleapiclient.discovery import build
from auth import get_credentials
import os
from datetime import datetime, timezone

CALENDAR_OWNER = os.getenv("CALENDAR_OWNER", "jc@rayze.xyz")
READ_ACCOUNTS = os.getenv("READ_ACCOUNTS", "").split(",")

CALENDAR_READ_SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events",
]

def get_calendar_service(user_email: str):
    creds = get_credentials(user_email, CALENDAR_READ_SCOPES)
    return build("calendar", "v3", credentials=creds)

def list_upcoming_events(user_email: str, max_results: int = 20):
    """List upcoming calendar events for a user (read-only)."""
    service = get_calendar_service(user_email)
    now = datetime.now(timezone.utc).isoformat()

    events_result = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    return events_result.get("items", [])

def create_event_on_jc(summary: str, start_dt: str, end_dt: str,
                        description: str = "", attendees: list = None):
    """
    Create a calendar event on jc@rayze.xyz ONLY.
    start_dt and end_dt should be ISO 8601 strings, e.g. '2026-02-20T14:00:00-05:00'
    """
    service = get_calendar_service(CALENDAR_OWNER)

    event_body = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_dt, "timeZone": "America/New_York"},
        "end": {"dateTime": end_dt, "timeZone": "America/New_York"},
    }

    if attendees:
        event_body["attendees"] = [{"email": a} for a in attendees]

    event = service.events().insert(
        calendarId="primary",
        body=event_body
    ).execute()

    print(f"Event created on {CALENDAR_OWNER}: {event.get('htmlLink')}")
    return event

def consolidate_calendars():
    """
    Read events from all accounts and copy new ones to jc@rayze.xyz calendar.
    This is the 'unite all calendar entries to jc@rayze.xyz' function.
    """
    jc_service = get_calendar_service(CALENDAR_OWNER)
    now = datetime.now(timezone.utc).isoformat()

    # Get existing event summaries on jc to avoid duplicates
    existing = jc_service.events().list(
        calendarId="primary",
        timeMin=now,
        singleEvents=True,
        orderBy="startTime",
        maxResults=250
    ).execute().get("items", [])

    existing_ids = {e.get("extendedProperties", {}).get("private", {}).get("sourceId")
                    for e in existing if e.get("extendedProperties")}

    for account in READ_ACCOUNTS:
        if account == CALENDAR_OWNER:
            continue  # Skip jc itself
        try:
            read_service = get_calendar_service(account)
            events = read_service.events().list(
                calendarId="primary",
                timeMin=now,
                singleEvents=True,
                orderBy="startTime",
                maxResults=50
            ).execute().get("items", [])

            for event in events:
                source_id = event["id"]
                if source_id in existing_ids:
                    continue  # Already consolidated

                start = event.get("start", {})
                end = event.get("end", {})

                new_event = {
                    "summary": f"[{account}] {event.get('summary', 'No title')}",
                    "description": f"Consolidated from {account}\\n\\n{event.get('description', '')}",
                    "start": start,
                    "end": end,
                    "extendedProperties": {
                        "private": {
                            "sourceId": source_id,
                            "sourceAccount": account
                        }
                    }
                }

                jc_service.events().insert(
                    calendarId="primary",
                    body=new_event
                ).execute()
                print(f"Consolidated: [{account}] {event.get('summary')}")

        except Exception as e:
            print(f"Could not read calendar for {account}: {e}")
