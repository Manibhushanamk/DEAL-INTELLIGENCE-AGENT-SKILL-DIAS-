import pytest
from src.memory.hindsight_client import HindsightClient
from src.setup_wizard import SetupWizard

def test_missing_api_key():
    client = HindsightClient(api_key="")
    client.api_key = ""
    valid, msg = client.validate_connection()
    assert valid is False
    assert "missing" in msg.lower()

def test_invalid_api_key():
    client = HindsightClient(api_key="hsk_invalid_bogus_key_1234567890abcdef")
    valid, msg = client.validate_connection()
    assert valid is False
    assert "Invalid Hindsight Cloud API key" in msg or "Authentication failed" in msg
    assert "hsk_invalid_bogus_key" not in msg

def test_missing_memory_bank_graceful():
    client = HindsightClient()
    recalled = client.recall(memory_bank_id="non_existent_bank_xyz_9999", query="test")
    assert isinstance(recalled, list)

def test_network_failure_handling():
    client = HindsightClient(api_key="hsk_test", base_url="https://nonexistent-domain-xyz-404.vectorize.io")
    valid, msg = client.validate_connection()
    assert valid is False
    assert "failed" in msg.lower()

def test_retain_failure_handling():
    client = HindsightClient(api_key="hsk_test", base_url="http://127.0.0.1:9")
    res = client.retain(memory_bank_id="test_bank", key="k1", data={"content": "data"})
    assert res["cloud_synced"] is False
    assert res["status"] == "failed"

def test_recall_failure_handling():
    client = HindsightClient(api_key="hsk_test", base_url="http://127.0.0.1:9")
    res = client.recall(memory_bank_id="test_bank", query="something")
    assert isinstance(res, list)

def test_reflect_failure_handling():
    client = HindsightClient(api_key="hsk_test", base_url="http://127.0.0.1:9")
    res = client.reflect(memory_bank_id="test_bank", topic="compliance")
    assert res["cloud_reflection"] is None
    assert isinstance(res["consolidated_beliefs"], list)

def test_setup_wizard_aborts_on_invalid_key():
    wizard = SetupWizard(unattended=True, api_key="hsk_invalid_key_9999")
    results = wizard.execute()
    assert results["hindsight_connected"] is False
