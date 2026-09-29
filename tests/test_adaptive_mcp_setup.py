import pytest
from src.setup_wizard import detect_host_agent, SetupWizard
from src.telemetry_analyzer import TelemetryAnalyzer
from mcp.adaptive_router import AdaptiveRouter
from src.memory.hindsight_client import HindsightClient

def test_host_detection():
    host_info = detect_host_agent()
    assert "name" in host_info
    assert "id" in host_info
    assert "mcp_transport" in host_info
    assert host_info["mcp_transport"] == "stdio"

def test_setup_wizard_unattended():
    wizard = SetupWizard(unattended=True)
    results = wizard.execute()
    assert results["hindsight_connected"] is True
    assert "dias_deals" in results["memory_banks"]
    assert results["triad_validation"]["all_passed"] is True

def test_telemetry_and_adaptive_recommendations():
    client = HindsightClient(api_key="mock_adaptive_test")
    telemetry = TelemetryAnalyzer(client)
    router = AdaptiveRouter(client, telemetry)

    # Simulate Day 1: General queries
    telemetry.record_interaction("What deals are closing in Q4?", interaction_day=1)
    
    # Simulate Day 5: 3 database queries
    telemetry.record_interaction("Query PostgreSQL deals table for discount history", interaction_day=5)
    telemetry.record_interaction("Check database schema for pipeline forecasts", interaction_day=5)
    telemetry.record_interaction("Execute SQL query on Neon database", interaction_day=5)

    # Analyze patterns
    analysis = telemetry.analyze_patterns()
    assert analysis["pattern_counts"]["database_queries"] >= 3
    assert len(analysis["friction_flags"]) >= 1

    # Check adaptive recommendations
    recs = router.get_recommendations()
    assert len(recs) > 0
    rec_ids = [r["id"] for r in recs]
    assert "neon_postgresql" in rec_ids

    # Connect recommended MCP
    conn_res = router.connect_mcp("neon_postgresql")
    assert conn_res["status"] == "connected"
    assert "neon_postgresql" in router.connected_mcps
    assert router.connected_mcps["neon_postgresql"]["transport"] == "stdio"
