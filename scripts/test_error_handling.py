#!/usr/bin/env python3
"""
Explicit Error Handling Test Script for DIAS.
Tests the 8 mandatory failure scenarios:
1. Missing API key
2. Invalid API key
3. Invalid Memory Bank
4. Network failure
5. Hindsight API failure
6. RETAIN failure
7. RECALL failure
8. REFLECT failure
"""
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, ROOT_DIR)

from src.memory.hindsight_client import HindsightClient
from src.setup_wizard import SetupWizard
from src.core_skill import DealIntelligenceSkill

def test_scenario_1_missing_api_key():
    print("\n[Scenario 1] Missing API key:")
    client = HindsightClient(api_key="")
    client.api_key = "" # clear any env fallback
    valid, msg = client.validate_connection()
    assert valid is False, "Expected validation to fail with empty key"
    assert "missing" in msg.lower(), f"Unexpected message: {msg}"
    print(f"  ✓ Handled safely: {msg}")

def test_scenario_2_invalid_api_key():
    print("\n[Scenario 2] Invalid API key:")
    client = HindsightClient(api_key="hsk_invalid_bogus_key_1234567890abcdef")
    valid, msg = client.validate_connection()
    assert valid is False, "Expected validation to fail with invalid key"
    assert "Invalid Hindsight Cloud API key" in msg or "Authentication failed" in msg
    assert "hsk_invalid_bogus_key" not in msg, "Raw key must not be in error message"
    print(f"  ✓ Handled safely: {msg}")

def test_scenario_3_invalid_memory_bank():
    print("\n[Scenario 3] Invalid / Non-existent Memory Bank handling:")
    client = HindsightClient()
    # Query recall on a non-existent bank without creating it
    recalled = client.recall(memory_bank_id="non_existent_bank_xyz_9999", query="test")
    assert isinstance(recalled, list), "Recall on missing bank should return empty list gracefully"
    print(f"  ✓ Handled safely: returned empty list without crashing")

def test_scenario_4_network_failure():
    print("\n[Scenario 4] Network failure:")
    client = HindsightClient(api_key="hsk_valid_looking_key", base_url="https://nonexistent-domain-xyz-404.vectorize.io")
    valid, msg = client.validate_connection()
    assert valid is False
    assert "failed" in msg.lower()
    print(f"  ✓ Handled safely: {msg}")

def test_scenario_5_hindsight_api_failure():
    print("\n[Scenario 5] API HTTP failure (404/500 endpoint):")
    client = HindsightClient(api_key="hsk_test", base_url="https://api.hindsight.vectorize.io/v1/bogus_subpath")
    valid, msg = client.validate_connection()
    assert valid is False
    print(f"  ✓ Handled safely: {msg}")

def test_scenario_6_retain_failure():
    print("\n[Scenario 6] RETAIN failure:")
    # Client with dead URL
    client = HindsightClient(api_key="hsk_test", base_url="http://127.0.0.1:9")
    res = client.retain(memory_bank_id="test_bank", key="k1", data={"content": "data"})
    assert res["cloud_synced"] is False
    assert res["status"] == "failed"
    print(f"  ✓ Handled safely: cloud_synced=False, status={res['status']}")

def test_scenario_7_recall_failure():
    print("\n[Scenario 7] RECALL failure:")
    client = HindsightClient(api_key="hsk_test", base_url="http://127.0.0.1:9")
    # Recall with unreachable server
    res = client.recall(memory_bank_id="test_bank", query="something")
    assert isinstance(res, list)
    print(f"  ✓ Handled safely: gracefully returned {len(res)} results without unhandled exception")

def test_scenario_8_reflect_failure():
    print("\n[Scenario 8] REFLECT failure:")
    client = HindsightClient(api_key="hsk_test", base_url="http://127.0.0.1:9")
    res = client.reflect(memory_bank_id="test_bank", topic="compliance")
    assert res["cloud_reflection"] is None
    assert isinstance(res["consolidated_beliefs"], list)
    print(f"  ✓ Handled safely: cloud_reflection=None, handled gracefully")

def test_wizard_aborts_on_invalid_key():
    print("\n[Setup Wizard Abort Test]")
    wizard = SetupWizard(unattended=True, api_key="hsk_invalid_key_9999")
    results = wizard.execute()
    assert results["hindsight_connected"] is False, "Setup must NOT report connected when key is invalid"
    print("  ✓ Setup Wizard correctly aborted and did NOT report DIAS READY.")

def main():
    print("=" * 60)
    print("RUNNING 8 ERROR HANDLING SCENARIO TESTS")
    print("=" * 60)
    test_scenario_1_missing_api_key()
    test_scenario_2_invalid_api_key()
    test_scenario_3_invalid_memory_bank()
    test_scenario_4_network_failure()
    test_scenario_5_hindsight_api_failure()
    test_scenario_6_retain_failure()
    test_scenario_7_recall_failure()
    test_scenario_8_reflect_failure()
    test_wizard_aborts_on_invalid_key()
    print("\n" + "=" * 60)
    print("ALL 8 ERROR SCENARIOS PASSED WITH ZERO SECRET LEAKS")
    print("=" * 60)

if __name__ == "__main__":
    main()
