import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from src.workspace.google_suite import GoogleWorkspaceSuite

class WorkspaceManager:
    """
    Safely bridges Google Workspace and messaging actions.
    Enforces Human-in-the-Loop governance:
    - Creates real Gmail drafts (does not auto-send without confirmation)
    - Schedules Google Calendar holds with duplicate prevention
    - Generates Google Docs executive dossiers
    - Syncs rows into the Master Deal Tracker Google Sheet
    """
    def __init__(self, client_secret_path: Optional[str] = None):
        self.google_suite = GoogleWorkspaceSuite(client_secret_path=client_secret_path)
        self.staged_actions: List[Dict[str, Any]] = []

    def is_google_connected(self) -> bool:
        return self.google_suite.is_connected()

    def initiate_oauth(self, open_browser: bool = True):
        return self.google_suite.auth.initiate_authorization_flow(open_browser=open_browser)

    def stage_followup_email(
        self,
        recipient_email: str,
        subject: str,
        body_text: str,
        deal_id: str,
        attachments: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Creates a real Gmail draft if authorized, and stages with human-in-the-loop review.
        """
        gmail_res = self.google_suite.gmail.create_draft(recipient_email, subject, body_text)
        action = {
            "action_id": f"act_mail_{len(self.staged_actions) + 1}",
            "type": "gmail_draft",
            "deal_id": deal_id,
            "recipient": recipient_email,
            "subject": subject,
            "body": body_text,
            "attachments": attachments or [],
            "status": "DRAFT_READY" if gmail_res.get("status") == "DRAFT_CREATED" else "STAGED_FOR_APPROVAL",
            "draft_id": gmail_res.get("draft_id"),
            "web_url": gmail_res.get("web_url"),
            "requires_human_approval": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        self.staged_actions.append(action)
        return action

    def stage_calendar_hold(
        self,
        meeting_title: str,
        attendees: List[str],
        duration_minutes: int,
        proposed_time: str,
        deal_id: str
    ) -> Dict[str, Any]:
        """
        Creates a real calendar event hold with duplicate prevention.
        """
        cal_res = self.google_suite.calendar.schedule_meeting(
            title=meeting_title,
            duration_minutes=duration_minutes,
            attendees=attendees,
            description=f"DIAS Deal Alignment for {deal_id}. Proposed time: {proposed_time}"
        )
        action = {
            "action_id": f"act_cal_{len(self.staged_actions) + 1}",
            "type": "calendar_hold",
            "deal_id": deal_id,
            "title": meeting_title,
            "attendees": attendees,
            "duration_minutes": duration_minutes,
            "proposed_time": proposed_time,
            "status": "EVENT_CREATED" if cal_res.get("status") == "CREATED" else "STAGED_FOR_APPROVAL",
            "event_id": cal_res.get("event_id"),
            "html_link": cal_res.get("html_link"),
            "requires_human_approval": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        self.staged_actions.append(action)
        return action

    def create_deal_doc(
        self,
        title: str,
        deal_data: Dict[str, Any],
        analytics: Dict[str, Any],
        battlecard: Dict[str, Any],
        reflections: List[str]
    ) -> Dict[str, Any]:
        """Creates an executive Google Doc dossier."""
        return self.google_suite.docs.create_deal_dossier_doc(
            title=title,
            deal_data=deal_data,
            analytics=analytics,
            battlecard=battlecard,
            reflections=reflections
        )

    def sync_deal_sheet(
        self,
        deal_data: Dict[str, Any],
        analytics: Dict[str, Any],
        doc_url: str = ""
    ) -> Dict[str, Any]:
        """Ensures master sheet exists and syncs deal record row."""
        sheet_info = self.google_suite.sheets.get_or_create_master_sheet()
        sheet_id = sheet_info.get("sheet_id", "simulated_master_deal_sheet_id")
        sync_res = self.google_suite.sheets.sync_deal_row(
            sheet_id=sheet_id,
            deal_data=deal_data,
            analytics=analytics,
            doc_url=doc_url
        )
        return {
            "sheet_id": sheet_id,
            "sheet_url": sheet_info.get("web_url"),
            "sync_status": sync_res.get("status")
        }

    def get_staged_actions(self, deal_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns list of staged actions, optionally filtered by deal_id."""
        if deal_id:
            return [a for a in self.staged_actions if a.get("deal_id") == deal_id]
        return self.staged_actions
