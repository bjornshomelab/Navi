from __future__ import print_function
import os, datetime, pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Exempel: Calendar scope (du kan byta ut mot Gmail, Drive, osv)
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/contacts"
]

def main():
    creds = None
    if os.path.exists("token.pkl"):
        with open("token.pkl", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pkl", "wb") as token:
            pickle.dump(creds, token)

    service = build("calendar", "v3", credentials=creds)

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    events_result = service.events().list(
        calendarId="primary", timeMin=now,
        maxResults=5, singleEvents=True, orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])
    if not events:
        print("Inga kommande events.")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])

if __name__ == "__main__":
    main()
