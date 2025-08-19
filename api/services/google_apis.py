"""
JARVIS AI Agent - Google APIs Service
Handles Gmail, Calendar, Drive, and other Google services
"""
import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from typing import Dict, Any, List
import datetime

class GoogleAPIService:
    """Service for Google APIs integration"""
    
    def __init__(self):
        self.scopes = [
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/gmail.modify",
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/contacts"
        ]
        self.credentials = self._get_credentials()
        
    def _get_credentials(self):
        """Get Google API credentials"""
        creds = None
        token_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "token.pkl")
        credentials_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "credentials.json")
        
        if os.path.exists(token_path):
            with open(token_path, "rb") as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(credentials_path):
                    raise FileNotFoundError(f"credentials.json not found at {credentials_path}")
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, self.scopes)
                creds = flow.run_local_server(port=0)
            
            with open(token_path, "wb") as token:
                pickle.dump(creds, token)
        
        return creds
    
    async def execute_action(self, action: str) -> str:
        """Execute a Google API action"""
        try:
            if ":" in action:
                action_type, description = action.split(":", 1)
                action_type = action_type.strip()
                description = description.strip()
            else:
                description = action
            
            desc_lower = description.lower()
            
            # Calendar operations
            if any(word in desc_lower for word in ["calendar", "meeting", "event", "schedule"]):
                return await self._handle_calendar_action(description)
            
            # Gmail operations
            elif any(word in desc_lower for word in ["email", "gmail", "mail", "message"]):
                return await self._handle_gmail_action(description)
            
            # Drive operations
            elif any(word in desc_lower for word in ["drive", "file", "document", "folder"]):
                return await self._handle_drive_action(description)
            
            else:
                return "Google API action type not recognized"
                
        except Exception as e:
            return f"Google API action failed: {str(e)}"
    
    async def _handle_calendar_action(self, description: str) -> str:
        """Handle calendar-related actions"""
        try:
            service = build("calendar", "v3", credentials=self.credentials)
            desc_lower = description.lower()
            
            if "list" in desc_lower or "show" in desc_lower or "events" in desc_lower:
                # List upcoming events
                now = datetime.datetime.now(datetime.timezone.utc).isoformat()
                events_result = service.events().list(
                    calendarId="primary", 
                    timeMin=now,
                    maxResults=5, 
                    singleEvents=True, 
                    orderBy="startTime"
                ).execute()
                
                events = events_result.get("items", [])
                if not events:
                    return "No upcoming events found"
                
                event_list = []
                for event in events:
                    start = event["start"].get("dateTime", event["start"].get("date"))
                    event_list.append(f"- {event['summary']} at {start}")
                
                return f"Upcoming events:\n" + "\n".join(event_list)
            
            else:
                return "Calendar action not yet implemented"
                
        except Exception as e:
            return f"Calendar action failed: {str(e)}"
    
    async def _handle_gmail_action(self, description: str) -> str:
        """Handle Gmail-related actions"""
        try:
            service = build("gmail", "v1", credentials=self.credentials)
            desc_lower = description.lower()
            
            if "list" in desc_lower or "show" in desc_lower or "recent" in desc_lower:
                # List recent emails
                results = service.users().messages().list(
                    userId="me", 
                    maxResults=5
                ).execute()
                
                messages = results.get("messages", [])
                if not messages:
                    return "No emails found"
                
                email_list = []
                for msg in messages[:3]:  # Limit to 3 for brevity
                    message = service.users().messages().get(userId="me", id=msg["id"]).execute()
                    payload = message["payload"]
                    headers = payload.get("headers", [])
                    
                    subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
                    sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown Sender")
                    
                    email_list.append(f"- {subject} from {sender}")
                
                return f"Recent emails:\n" + "\n".join(email_list)
            
            else:
                return "Gmail action not yet implemented"
                
        except Exception as e:
            return f"Gmail action failed: {str(e)}"
    
    async def _handle_drive_action(self, description: str) -> str:
        """Handle Google Drive actions"""
        try:
            service = build("drive", "v3", credentials=self.credentials)
            desc_lower = description.lower()
            
            if "list" in desc_lower or "show" in desc_lower or "files" in desc_lower:
                # List recent files
                results = service.files().list(
                    pageSize=5, 
                    fields="nextPageToken, files(id, name, mimeType, modifiedTime)"
                ).execute()
                
                files = results.get("files", [])
                if not files:
                    return "No files found in Drive"
                
                file_list = []
                for file in files:
                    file_list.append(f"- {file['name']} ({file.get('mimeType', 'unknown type')})")
                
                return f"Recent Drive files:\n" + "\n".join(file_list)
            
            else:
                return "Drive action not yet implemented"
                
        except Exception as e:
            return f"Drive action failed: {str(e)}"
