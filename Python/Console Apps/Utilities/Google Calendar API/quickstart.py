from __future__ import print_function

import datetime
import os
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Keep OAuth client material and per-user refresh tokens outside source control.
SCRIPT_DIR = Path(__file__).resolve().parent
CLIENT_SECRETS_FILE = Path(
    os.environ.get(
        "GOOGLE_CALENDAR_CLIENT_SECRETS_FILE",
        str(SCRIPT_DIR / "credentials.json"),
    )
)
TOKEN_FILE = Path(
    os.environ.get("GOOGLE_CALENDAR_TOKEN_FILE", str(SCRIPT_DIR / "token.json"))
)
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def main():
    """Print the next ten events from the authenticated user's calendar."""
    creds = None
    if TOKEN_FILE.is_file():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRETS_FILE.is_file():
                raise FileNotFoundError(
                    "Google OAuth client JSON is missing. Place the rotated file "
                    "outside source control or set GOOGLE_CALENDAR_CLIENT_SECRETS_FILE."
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRETS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")

    service = build("calendar", "v3", credentials=creds)
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    print("Getting the upcoming 10 events")
    events_result = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=10,
        singleEvents=True,
        orderBy="startTime",
    ).execute()
    events = events_result.get("items", [])

    if not events:
        print("No upcoming events found.")
        return

    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event.get("summary", "(untitled event)"))


if __name__ == "__main__":
    main()
