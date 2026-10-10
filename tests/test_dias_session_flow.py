import os
import pytest
from src.session.controller import DiasSessionController

def test_dias_command_session_initialization():
    controller = DiasSessionController()
    res = controller.handle_dias_command(
        user_input="We have a $350k deal with Acme Corp in Security Review. Competitor is Gong. Target close End of Q4."
    )
    assert res["command"] == "/dias"
    assert res["status"] == "COLLECTING_INPUT"
    assert "integrations" in res
    assert "deal_profile" in res
    assert res["deal_profile"]["customer"] == "Acme Corp"
    assert res["deal_profile"]["value"] == 350000.0
    assert "validation" in res

def test_dias_input_end_execution():
    controller = DiasSessionController()
    # Step 1: Input deal info
    controller.handle_dias_command(
        user_input="We have a $350k deal with Acme Corp. VP of Security requires AWS GovCloud and Okta SSO. Competitor Gong. Budget approved."
    )
    # Step 2: Trigger input end
    res = controller.handle_dias_input_end_command()
    assert res["command"] == "/dias-input-end"
    assert res["status"] == "COMPLETED"
    assert "deliverables" in res
    assert "pdf_dossier" in res["deliverables"]
    assert os.path.exists(res["deliverables"]["pdf_dossier"])
    assert "google_doc" in res["deliverables"]
    assert "master_google_sheet" in res["deliverables"]
    assert "gmail_draft" in res["deliverables"]
    assert "calendar_hold" in res["deliverables"]
    assert "persistence" in res
    assert "next_actions" in res
