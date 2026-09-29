import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

class WorkspaceManager:
    """
    Safely stages Google Workspace and messaging actions.
    Enforces strict Human-in-the-Loop governance: all Gmail drafts and Calendar invitations
    are staged in draft/holding status and require explicit human review before dispatch.
    """
    def __init__(self):
        self.staged_actions: List[Dict[str, Any]] = []

    def stage_followup_email(
        self,
        recipient_email: str,
        subject: str,
        body_text: str,
        deal_id: str,
        attachments: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Stages a follow-up email draft in Gmail with human-in-the-loop safety gating.
        """
        action = {
            "action_id": f"act_mail_{len(self.staged_actions) + 1}",
            "type": "gmail_draft",
            "deal_id": deal_id,
            "recipient": recipient_email,
            "subject": subject,
            "body": body_text,
            "attachments": attachments or [],
            "status": "STAGED_FOR_APPROVAL",
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
        Stages an executive calendar meeting hold in Google Calendar with human review.
        """
        action = {
            "action_id": f"act_cal_{len(self.staged_actions) + 1}",
            "type": "calendar_hold",
            "deal_id": deal_id,
            "title": meeting_title,
            "attendees": attendees,
            "duration_minutes": duration_minutes,
            "proposed_time": proposed_time,
            "status": "STAGED_FOR_APPROVAL",
            "requires_human_approval": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        self.staged_actions.append(action)
        return action

    def get_staged_actions(self, deal_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns list of staged actions, optionally filtered by deal_id."""
        if deal_id:
            return [a for a in self.staged_actions if a.get("deal_id") == deal_id]
        return self.staged_actions
