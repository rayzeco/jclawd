"""
Run this to verify every permission works correctly.
"""
from dotenv import load_dotenv
load_dotenv()

import os
from gmail_client import list_unread_messages, get_message_details, send_email
from calendar_client import list_upcoming_events, consolidate_calendars
from drive_client import search_docs, list_recent_docs

READ_ACCOUNTS = os.getenv("READ_ACCOUNTS", "").split(",")
BOT_EMAIL = os.getenv("BOT_EMAIL", "ai@rayze.xyz")
CALENDAR_OWNER = os.getenv("CALENDAR_OWNER", "jc@rayze.xyz")

def test_gmail_read():
    print("\\n=== TESTING GMAIL READ ===")
    for account in READ_ACCOUNTS:
        print(f"\\n--- {account} ---")
        try:
            messages = list_unread_messages(account, max_results=3)
            print(f"  Unread count: {len(messages)}")
            for msg in messages[:2]:
                details = get_message_details(account, msg["id"])
                print(f"  From: {details['from']}")
                print(f"  Subject: {details['subject']}")
                print(f"  Snippet: {details['snippet'][:80]}...")
        except Exception as e:
            print(f"  ERROR: {e}")

def test_gmail_send():
    print("\\n=== TESTING GMAIL SEND (from ai@rayze.xyz only) ===")
    try:
        send_email(
            to=BOT_EMAIL,  # Send to itself as test
            subject="Bot Test Email",
            body="This is a test email from the Rayze bot. If you see this, send is working!"
        )
        print("  SUCCESS: Email sent")
    except Exception as e:
        print(f"  ERROR: {e}")

def test_calendar_read():
    print("\\n=== TESTING CALENDAR READ ===")
    try:
        events = list_upcoming_events(CALENDAR_OWNER, max_results=5)
        print(f"  {CALENDAR_OWNER} has {len(events)} upcoming events")
        for e in events[:3]:
            start = e.get("start", {}).get("dateTime", e.get("start", {}).get("date"))
            print(f"  - {e.get('summary', 'No title')} at {start}")
    except Exception as e:
        print(f"  ERROR: {e}")

def test_calendar_consolidation():
    print("\\n=== TESTING CALENDAR CONSOLIDATION ===")
    try:
        consolidate_calendars()
        print("  Consolidation complete")
    except Exception as e:
        print(f"  ERROR: {e}")

def test_drive_read():
    print("\\n=== TESTING DRIVE READ ===")
    try:
        files = list_recent_docs(max_results=5)
        print(f"  Found {len(files)} recent files in jc@rayze.xyz Drive")
        for f in files[:3]:
            print(f"  - {f['name']} ({f['mimeType']})")
    except Exception as e:
        print(f"  ERROR: {e}")

if __name__ == "__main__":
    test_gmail_read()
    test_gmail_send()
    test_calendar_read()
    test_calendar_consolidation()
    test_drive_read()
    print("\\n=== ALL TESTS COMPLETE ===")
