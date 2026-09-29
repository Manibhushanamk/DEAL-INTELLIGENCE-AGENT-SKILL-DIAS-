import pytest
from src.memory.hindsight_client import HindsightClient

def test_hindsight_key_masking():
    assert HindsightClient.mask_key("hsk_mockkey1234567890abcdef12345678_9999") == "hsk_...9999"
    assert HindsightClient.mask_key(None) == "[NONE]"
    assert HindsightClient.mask_key("short") == "****"

def test_hindsight_validation():
    client = HindsightClient()
    valid, msg = client.validate_connection()
    assert isinstance(valid, bool)
    assert isinstance(msg, str)
    assert len(msg) > 0

def test_hindsight_retain_recall():
    client = HindsightClient()
    test_bank = "test_deals_bank"
    
    # 1. Retain
    fact = {
        "deal_id": "DEAL-TEST-001",
        "customer": "TestCorp",
        "event_type": "security_briefing",
        "content": "TestCorp mandates Okta SSO SAML 2.0 integration and SOC2 compliance."
    }
    retain_res = client.retain(memory_bank_id=test_bank, key="test_doc_1", data=fact)
    assert retain_res["status"] == "success"
    assert retain_res["key"] == "test_doc_1"

    # 2. Recall
    recalled = client.recall(memory_bank_id=test_bank, query="What SSO integration is needed?", top_k=3)
    assert len(recalled) > 0
    assert "okta" in str(recalled).lower() or "testcorp" in str(recalled).lower()

def test_hindsight_reflect():
    client = HindsightClient()
    test_bank = "test_deals_bank"
    
    reflect_res = client.reflect(memory_bank_id=test_bank, topic="security_and_sso")
    assert reflect_res["status"] == "success"
    assert "consolidated_beliefs" in reflect_res
    assert len(reflect_res["consolidated_beliefs"]) > 0

def test_preflight_triad_health_check():
    client = HindsightClient()
    report = client.execute_preflight_triad(bank_id="dias_test_triad")
    assert report["status"] == "PASSED"
    assert report["all_passed"] is True
    assert report["triad"]["retain"]["passed"] is True
    assert report["triad"]["recall"]["passed"] is True
    assert report["triad"]["reflect"]["passed"] is True
