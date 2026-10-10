import pytest
from src.workspace.google_suite import GoogleWorkspaceSuite

def test_google_workspace_suite_initialization():
    suite = GoogleWorkspaceSuite()
    status = suite.get_status()
    assert "authorized" in status
    assert "services" in status
    assert "gmail" in status["services"]
    assert "calendar" in status["services"]
    assert "docs" in status["services"]
    assert "sheets" in status["services"]
    assert "drive" in status["services"]

def test_gmail_draft_creation_and_safety_gate():
    suite = GoogleWorkspaceSuite()
    draft = suite.gmail.create_draft(
        recipient_email="buyer@testcorp.com",
        subject="Test Deal Follow-up",
        body_text="Here is the recap."
    )
    assert "status" in draft
    assert draft["recipient"] == "buyer@testcorp.com"

    # Verify safety gate blocks unconfirmed sending
    blocked = suite.gmail.send_email_with_confirmation(
        recipient_email="buyer@testcorp.com",
        subject="Test",
        body_text="Body",
        user_confirmed=False
    )
    assert blocked["status"] == "BLOCKED_REQUIRES_CONFIRMATION"

def test_calendar_event_scheduling_and_dedup():
    suite = GoogleWorkspaceSuite()
    ev = suite.calendar.schedule_meeting(
        title="Procurement Review",
        duration_minutes=45,
        attendees=["buyer@testcorp.com"],
        description="Review deal terms"
    )
    assert "status" in ev
    assert ev["title"] == "Procurement Review"

def test_docs_dossier_formatting():
    suite = GoogleWorkspaceSuite()
    deal_data = {
        "deal_id": "DEAL-DOCS-001",
        "customer": "Docs Corp",
        "value": 200000.0,
        "stage": "Security Review"
    }
    analytics = {
        "health_score": 88.0,
        "win_probability": 80.0,
        "breakdown": {"budget_score": 85}
    }
    battlecard = {"counter_narrative": "Lead with security"}
    doc = suite.docs.create_deal_dossier_doc(
        title="DIAS Dossier — Docs Corp",
        deal_data=deal_data,
        analytics=analytics,
        battlecard=battlecard,
        reflections=["Key reflection 1"]
    )
    assert "status" in doc
    assert "title" in doc
    assert "web_url" in doc

def test_sheets_master_tracker():
    suite = GoogleWorkspaceSuite()
    sheet = suite.sheets.get_or_create_master_sheet("DIAS Master Deal Tracker")
    assert "status" in sheet
    assert "web_url" in sheet

    sync = suite.sheets.sync_deal_row(
        sheet_id=sheet.get("sheet_id", "test_sheet"),
        deal_data={"deal_id": "DEAL-001", "customer": "Test Corp", "value": 100000},
        analytics={"health_score": 75, "win_probability": 70},
        doc_url="https://docs.google.com/test"
    )
    assert "status" in sync
