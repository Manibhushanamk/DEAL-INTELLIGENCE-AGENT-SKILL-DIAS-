import os
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone

from src.session.deal_profile import NormalizedDealProfile
from src.database.neon_client import NeonClient
from src.memory.hindsight_client import HindsightClient
from src.analytics.deal_scorer import DealScorer
from src.narrative.battlecards import BattlecardEngine
from src.workspace.google_suite import GoogleWorkspaceSuite
from src.dossier.pdf_generator import PDFDossierGenerator

logger = logging.getLogger("DiasController")
logger.setLevel(logging.INFO)


class DiasSessionController:
    """
    Controller executing the two core DIAS commands:
    - `/dias`: Session initialization, integration auditing, OAuth check, input intake.
    - `/dias-input-end`: Input validation, memory recall, scoring, document generation,
                        Neon & Hindsight persistence, and workspace artifact synchronization.
    """

    def __init__(
        self,
        session_id: Optional[str] = None,
        neon_client: Optional[NeonClient] = None,
        hindsight_client: Optional[HindsightClient] = None,
        google_suite: Optional[GoogleWorkspaceSuite] = None
    ):
        if not session_id:
            session_file = os.path.join(os.getcwd(), ".dias_session")
            if os.path.exists(session_file):
                try:
                    with open(session_file, "r", encoding="utf-8") as f:
                        saved_id = f.read().strip()
                        if saved_id:
                            session_id = saved_id
                except Exception:
                    pass

        self.session_id = session_id or f"dias_sess_{int(datetime.now().timestamp())}"
        self.neon = neon_client or NeonClient()
        self.hindsight = hindsight_client or HindsightClient()
        self.google = google_suite or GoogleWorkspaceSuite()
        self.scorer = DealScorer()
        self.battlecards = BattlecardEngine()
        self.pdf_gen = PDFDossierGenerator()

        self.profile = NormalizedDealProfile()
        self.status = "INITIALIZED"
        self.last_result: Optional[Dict[str, Any]] = None

        # Check if an existing session can be resumed from Neon
        self._check_resume_session()

    def _check_resume_session(self) -> None:
        """Attempts to resume interrupted session state from Neon PostgreSQL."""
        existing = self.neon.get_session(self.session_id)
        if existing and existing.get("state_data"):
            state = existing["state_data"]
            self.status = existing.get("status", "ACTIVE")
            if "deal" in state:
                for k, v in state["deal"].items():
                    if hasattr(self.profile, k):
                        if k == "competition" and isinstance(v, str):
                            v = [c.strip() for c in v.split(",") if c.strip() and c.strip().lower() != "none"]
                        setattr(self.profile, k, v)

    def check_integrations(self) -> Dict[str, Any]:
        """Audits active connectivity to Hindsight Cloud, Neon DB, and Google Workspace."""
        hindsight_ok, hindsight_msg = self.hindsight.validate_connection()
        neon_ok, neon_msg, neon_counts = self.neon.health_check()
        google_connected = self.google.is_connected()
        return {
            "hindsight_cloud": {
                "status": "CONNECTED" if hindsight_ok else "OFFLINE",
                "message": hindsight_msg,
                "role": "Cognitive Brain & Persistent Memory"
            },
            "neon_postgresql": {
                "status": "CONNECTED" if neon_ok else "OFFLINE",
                "message": neon_msg,
                "role": "Authoritative Structured Deal Database",
                "tables_count": neon_counts
            },
            "google_workspace": {
                "status": "AUTHORIZED" if google_connected else "PENDING_OAUTH",
                "user_email": self.google.auth.user_email,
                "client_secret_configured": bool(self.google.auth.client_secret_path),
                "role": "Gmail Drafts, Calendar Holds, Docs & Master Sheet Sync"
            }
        }

    # =========================================================================
    # COMMAND 1: /dias
    # =========================================================================
    def handle_dias_command(
        self,
        user_input: Optional[str] = None,
        deal_id: Optional[str] = None,
        file_path: Optional[str] = None,
        interactive_oauth: bool = False
    ) -> Dict[str, Any]:
        """
        Executes `/dias`:
        1. Initialize/resume session state.
        2. Check integration availability (Neon, Hindsight, Google).
        3. If Google OAuth is missing, report or initiate.
        4. Ingest user notes, files, or deal ID.
        5. Maintain normalized deal profile.
        6. Return integration report, profile status, and targeted questions.
        """
        self.status = "COLLECTING_INPUT"

        # 1. Integration health audit
        hindsight_ok, hindsight_msg = self.hindsight.validate_connection()
        neon_ok, neon_msg, neon_counts = self.neon.health_check()
        google_connected = self.google.is_connected()

        # If user requests interactive OAuth trigger on /dias
        oauth_action = None
        if not google_connected and interactive_oauth:
            auth_ok, auth_msg = self.google.auth.initiate_authorization_flow()
            google_connected = self.google.is_connected()
            oauth_action = {"attempted": True, "success": auth_ok, "message": auth_msg}

        # 2. Ingest existing deal ID if provided
        if deal_id:
            self.profile.deal_id = deal_id
            existing_deal = self.neon.get_deal(deal_id)
            if existing_deal:
                self.profile.customer = existing_deal.get("customer", self.profile.customer)
                self.profile.value = float(existing_deal.get("value") or self.profile.value)
                self.profile.stage = existing_deal.get("stage", self.profile.stage)
                self.profile.verified_facts.append(f"Loaded existing deal record from Neon: {deal_id}")

        # 3. Ingest input file if provided
        if file_path:
            self.profile.ingest_file(file_path)

        # 4. Ingest natural language notes
        if user_input:
            self.profile.ingest_text(user_input, source="user_conversation")

        # 5. Save session state to Neon
        self._persist_session_state()

        # 6. Evaluate missing fields for targeted follow-ups
        validation = self.profile.validate_inputs()

        # Construct user-facing operational response
        integrations_status = {
            "hindsight_cloud": {
                "status": "CONNECTED" if hindsight_ok else "OFFLINE",
                "message": hindsight_msg,
                "role": "Cognitive Brain & Persistent Memory"
            },
            "neon_postgresql": {
                "status": "CONNECTED" if neon_ok else "OFFLINE",
                "message": neon_msg,
                "role": "Authoritative Structured Deal Database",
                "tables_count": neon_counts
            },
            "google_workspace": {
                "status": "AUTHORIZED" if google_connected else "PENDING_OAUTH",
                "user_email": self.google.auth.user_email,
                "client_secret_configured": bool(self.google.auth.client_secret_path),
                "role": "Gmail Drafts, Calendar Holds, Docs & Master Sheet Sync"
            }
        }

        return {
            "command": "/dias",
            "session_id": self.session_id,
            "status": self.status,
            "integrations": integrations_status,
            "oauth_action": oauth_action,
            "deal_profile": self.profile.to_dict(),
            "validation": validation,
            "next_step": "Provide additional deal details or run /dias-input-end to begin executive analysis."
        }

    # =========================================================================
    # COMMAND 2: /dias-input-end
    # =========================================================================
    def handle_dias_input_end_command(
        self,
        clarifications: Optional[Dict[str, Any]] = None,
        confirm_send_email: bool = False
    ) -> Dict[str, Any]:
        """
        Executes `/dias-input-end`:
        1. Validate inputs and handle missing fields.
        2. Recall past deal context and objections from Hindsight Cloud.
        3. Run multi-vector deal health scoring.
        4. Generate ReportLab executive PDF dossier.
        5. Generate Google Doc executive report.
        6. Create or update Master Deal Tracker Google Sheet.
        7. Stage Gmail draft & Google Calendar hold.
        8. Persist all records into Neon PostgreSQL.
        9. Retain structured facts & telemetry in Hindsight Cloud.
        10. Return comprehensive executive summary.
        """
        # Apply any clarification inputs provided
        if clarifications:
            for k, v in clarifications.items():
                if hasattr(self.profile, k):
                    setattr(self.profile, k, v)
                elif k == "customer":
                    self.profile.customer = v
                elif k == "value":
                    self.profile.value = float(v)

        # 1. Validation check
        validation = self.profile.validate_inputs()
        deal_dict = self.profile.to_dict()

        # 2. Hindsight Memory Recall
        memory_query = f"{self.profile.customer} {self.profile.deal_id} security compliance budget competitor"
        historical_memories = self.hindsight.recall(
            namespace="dias_deals",
            query=memory_query,
            top_k=5
        )

        # Hindsight Reflection
        reflection = self.hindsight.reflect(
            namespace="dias_deals",
            topic=f"{self.profile.customer} deal closing strategy"
        )
        consolidated_beliefs = reflection.get("consolidated_beliefs", [])

        # 3. Deal Analysis & Scoring
        analytics = self.scorer.calculate_health(deal_dict, historical_memories=historical_memories)

        # Battlecard retrieval
        primary_competitor = self.profile.competition[0] if self.profile.competition else "Gong"
        battlecard = self.battlecards.get_battlecard(primary_competitor)

        # 4. Deliverable Generation: Executive PDF Dossier
        os.makedirs("reports", exist_ok=True)
        pdf_filename = f"reports/{self.profile.deal_id.lower().replace('-', '_')}_dossier.pdf"
        pdf_path = os.path.abspath(pdf_filename)
        self.pdf_gen.generate_dossier(
            output_filepath=pdf_path,
            account_name=self.profile.customer,
            deal_data=deal_dict,
            analytics_summary=analytics,
            battlecard=battlecard,
            hindsight_reflections=consolidated_beliefs
        )

        # 5. Deliverable Generation: Google Doc Report
        doc_title = f"DIAS Deal Dossier — {self.profile.customer} ({self.profile.deal_id})"
        doc_result = self.google.docs.create_deal_dossier_doc(
            title=doc_title,
            deal_data=deal_dict,
            analytics=analytics,
            battlecard=battlecard,
            reflections=consolidated_beliefs
        )
        google_doc_url = doc_result.get("web_url")

        # 6. Deliverable Generation: Master Google Sheet Sync
        sheet_result = self.google.sheets.get_or_create_master_sheet()
        sheet_id = sheet_result.get("sheet_id", "simulated_master_sheet_id")
        self.google.sheets.sync_deal_row(
            sheet_id=sheet_id,
            deal_data=deal_dict,
            analytics=analytics,
            doc_url=google_doc_url or ""
        )
        google_sheet_url = sheet_result.get("web_url")

        # 7. Workspace Actions: Gmail Draft & Calendar Hold (Human-in-the-Loop)
        champion_email = f"champion@{self.profile.customer.lower().replace(' ', '')}.com"
        email_subject = f"Next Steps & Security Architecture Review — {self.profile.customer}"
        email_body = f"""Hi {self.profile.customer} Team,

Thank you for our productive discussion regarding your upcoming project.
Per our conversation, our architecture provides full support for:
- {', '.join(self.profile.requirements) if self.profile.requirements else 'SOC2 Type II and Okta SSO'}
- Dedicated tenant data isolation and persistent memory intelligence.

We have compiled your full Executive Account Dossier and staged our technical alignment review.

Best regards,
{self.profile.owner}
"""
        gmail_draft_res = self.google.gmail.create_draft(
            recipient_email=champion_email,
            subject=email_subject,
            body_text=email_body
        )

        meeting_title = f"{self.profile.customer} <> Architecture & Security Alignment"
        calendar_res = self.google.calendar.schedule_meeting(
            title=meeting_title,
            duration_minutes=30,
            attendees=[champion_email],
            description=f"Executive review for {self.profile.deal_id}. Deal Health: {analytics.get('health_score')}/100"
        )

        # 8. Neon PostgreSQL Persistence
        self.neon.save_deal(deal_dict)
        if self.profile.stakeholders:
            self.neon.save_stakeholders(self.profile.deal_id, self.profile.stakeholders)
        self.neon.record_interaction(
            deal_id=self.profile.deal_id,
            event_type="dias_analysis",
            content=f"Deal evaluated. Health: {analytics.get('health_score')}/100. Win Prob: {analytics.get('win_probability')}%."
        )
        if self.profile.risks:
            self.neon.save_risks(self.profile.deal_id, self.profile.risks)
        self.neon.save_assessment(self.profile.deal_id, analytics)

        # Save actions
        action_items = [
            {
                "action_type": "email_followup",
                "title": f"Send meeting recap to {self.profile.customer} champion",
                "description": f"Gmail draft created: {gmail_draft_res.get('draft_id', 'staged')}",
                "owner": self.profile.owner,
                "due_date": "Within 24 hours",
                "status": "DRAFT_READY"
            },
            {
                "action_type": "calendar_meeting",
                "title": meeting_title,
                "description": f"Calendar hold: {calendar_res.get('event_id', 'staged')}",
                "owner": self.profile.owner,
                "due_date": "Next Tuesday 2:00 PM",
                "status": "SCHEDULED"
            }
        ]
        self.neon.save_actions(self.profile.deal_id, action_items)

        # Save document references to Neon
        self.neon.save_document(
            deal_id=self.profile.deal_id,
            doc_type="PDF_DOSSIER",
            title=f"{self.profile.customer} Executive PDF Dossier",
            file_path=pdf_path,
            google_doc_url=google_doc_url,
            google_sheet_url=google_sheet_url
        )

        # 9. Vectorize Hindsight Cloud Persistence (RETAIN)
        hindsight_deal_fact = {
            "deal_id": self.profile.deal_id,
            "customer": self.profile.customer,
            "event_type": "executive_deal_assessment",
            "content": (
                f"Deal {self.profile.deal_id} for {self.profile.customer} valued at ${self.profile.value:,.2f}. "
                f"Stage: {self.profile.stage}. Health Score: {analytics.get('health_score')}/100. "
                f"Win Probability: {analytics.get('win_probability')}%. "
                f"Competitors: {', '.join(self.profile.competition) if self.profile.competition else 'None'}. "
                f"Requirements: {', '.join(self.profile.requirements) if self.profile.requirements else 'Standard'}. "
                f"Top Risks: {', '.join([r['description'] for r in self.profile.risks]) if self.profile.risks else 'None'}."
            ),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.hindsight.retain(
            namespace="dias_deals",
            key=f"dias_{self.profile.deal_id.lower()}_assessment",
            data=hindsight_deal_fact
        )

        self.hindsight.retain(
            namespace="dias_telemetry",
            key=f"telemetry_{self.session_id}",
            data={
                "session_id": self.session_id,
                "deal_id": self.profile.deal_id,
                "event": "dias_input_end_execution",
                "tools_used": ["deal_scorer", "reportlab_pdf", "google_workspace", "neon_db", "hindsight_cloud"]
            }
        )

        # 10. Update session status to COMPLETED
        self.status = "COMPLETED"
        self._persist_session_state()

        self.last_result = {
            "command": "/dias-input-end",
            "session_id": self.session_id,
            "status": self.status,
            "deal_id": self.profile.deal_id,
            "customer": self.profile.customer,
            "value": f"${self.profile.value:,.2f} {self.profile.currency}",
            "stage": self.profile.stage,
            "health_score": f"{analytics.get('health_score')}/100 ({analytics.get('health_tier')})",
            "win_probability": f"{analytics.get('win_probability')}%",
            "deliverables": {
                "pdf_dossier": pdf_path,
                "google_doc": google_doc_url or "Staged in local dossier",
                "master_google_sheet": google_sheet_url or "Staged in local tracker",
                "gmail_draft": gmail_draft_res.get("web_url") or f"Draft staged for {champion_email}",
                "calendar_hold": calendar_res.get("html_link") or f"Hold staged: {meeting_title}"
            },
            "persistence": {
                "neon_postgresql": "Authoritative structured records saved (deal, assessment, risks, actions, docs)",
                "hindsight_cloud": "Persistent cognitive retention completed in dias_deals & dias_telemetry"
            },
            "next_actions": action_items,
            "clarifications_remaining": validation["missing_essential_fields"]
        }
        return self.last_result

    def _persist_session_state(self) -> None:
        """Saves session state snapshot into Neon PostgreSQL."""
        state_data = {
            "deal": self.profile.to_dict(),
            "status": self.status,
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
        self.neon.save_session(
            session_id=self.session_id,
            deal_id=self.profile.deal_id,
            status=self.status,
            state_data=state_data
        )
        try:
            with open(os.path.join(os.getcwd(), ".dias_session"), "w", encoding="utf-8") as f:
                f.write(self.session_id)
        except Exception:
            pass
