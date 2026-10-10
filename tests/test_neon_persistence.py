import pytest
from src.database.neon_client import NeonClient

def test_neon_health_and_tables():
    client = NeonClient()
    ok, msg, counts = client.health_check()
    assert isinstance(ok, bool)
    assert isinstance(msg, str)
    assert "deals" in counts
    assert "deal_assessments" in counts

def test_neon_deal_lifecycle():
    client = NeonClient()
    test_deal_id = "DEAL-TEST-NEON-999"
    deal = {
        "deal_id": test_deal_id,
        "customer": "Test Enterprise Corp",
        "owner": "Account Exec",
        "value": 150000.0,
        "currency": "USD",
        "stage": "Discovery",
        "budget_status": "Approved",
        "competition": "Gong",
        "timeline": "Q4 2026",
        "verification_status": "verified"
    }

    # Save
    saved = client.save_deal(deal)
    assert saved["deal_id"] == test_deal_id
    assert saved["customer"] == "Test Enterprise Corp"

    # Fetch
    fetched = client.get_deal(test_deal_id)
    assert fetched is not None
    assert fetched["deal_id"] == test_deal_id
    assert float(fetched["value"]) == 150000.0

def test_neon_stakeholders_and_risks():
    client = NeonClient()
    deal_id = "DEAL-TEST-NEON-999"

    # Stakeholders
    shs = [
        {"name": "Alice Smith", "role": "CFO", "title": "CFO", "buying_authority": "Economic Buyer"}
    ]
    saved_shs = client.save_stakeholders(deal_id, shs)
    assert len(saved_shs) == 1

    fetched_shs = client.get_stakeholders(deal_id)
    assert len(fetched_shs) >= 1

    # Risks
    risks = [
        {"risk_type": "Security", "description": "Mandatory SOC2", "severity": "High", "mitigation": "Provide report"}
    ]
    saved_risks = client.save_risks(deal_id, risks)
    assert len(saved_risks) == 1

def test_neon_assessment_and_actions():
    client = NeonClient()
    deal_id = "DEAL-TEST-NEON-999"

    # Assessment
    assessment = {
        "health_score": 85.0,
        "win_probability": 78.0,
        "breakdown": {"budget": 90, "authority": 80},
        "model_version": "1.0.0"
    }
    client.save_assessment(deal_id, assessment)
    fetched_ass = client.get_latest_assessment(deal_id)
    assert fetched_ass is not None
    assert float(fetched_ass["overall_health"]) == 85.0

    # Actions
    actions = [
        {"action_type": "email", "title": "Followup recap", "owner": "AE", "due_date": "Tomorrow"}
    ]
    client.save_actions(deal_id, actions)
    fetched_acts = client.get_actions(deal_id)
    assert len(fetched_acts) >= 1

def test_neon_session_persistence():
    client = NeonClient()
    sess_id = "sess_neon_test_123"
    client.save_session(
        session_id=sess_id,
        deal_id="DEAL-TEST-NEON-999",
        status="ACTIVE",
        state_data={"step": "collecting"}
    )
    fetched_sess = client.get_session(sess_id)
    assert fetched_sess is not None
    assert fetched_sess["session_id"] == sess_id
    assert fetched_sess["status"] == "ACTIVE"
