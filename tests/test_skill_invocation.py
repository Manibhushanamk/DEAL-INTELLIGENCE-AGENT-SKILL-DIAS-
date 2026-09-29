import pytest
from src.core_skill import DealIntelligenceSkill
from mcp.server import MCPServer

@pytest.fixture
def skill():
    return DealIntelligenceSkill(api_key="mock_invocation_key")

@pytest.fixture
def mcp_server(skill):
    return MCPServer(skill=skill)

def test_skill_deal_analytics(skill):
    deal_data = {
        "deal_id": "DEAL-ACME-001",
        "customer": "Acme Corp",
        "amount": "$350,000",
        "stage": "Negotiation",
        "notes": "VP of Security confirmed Okta SSO and AWS GovCloud required. SOC2 Type II verified.",
        "stakeholders": [
            {"name": "Sarah Chen", "role": "VP of Security"},
            {"name": "Mark Roberts", "role": "Champion"}
        ]
    }
    result = skill.deal_analytics(deal_data)
    assert "overall_health_score" in result
    assert result["overall_health_score"] >= 70.0
    assert result["health_tier"] in ["HEALTHY", "EXCELLENT"]
    assert "win_probability_pct" in result

def test_skill_workspace_staging(skill):
    res_mail = skill.stage_workspace("email", {
        "deal_id": "DEAL-ACME-001",
        "recipient": "sarah.chen@acme.com",
        "subject": "Acme Corp Deal Follow-Up",
        "body": "Thank you for the productive review. Attached is the security dossier."
    })
    assert res_mail["status"] == "STAGED_FOR_APPROVAL"
    assert res_mail["requires_human_approval"] is True

    res_cal = skill.stage_workspace("calendar", {
        "deal_id": "DEAL-ACME-001",
        "title": "Acme Executive Review",
        "attendees": ["sarah.chen@acme.com"],
        "duration": 30,
        "time": "Tomorrow 3:00 PM EST"
    })
    assert res_cal["status"] == "STAGED_FOR_APPROVAL"

def test_mcp_server_listing_and_execution(mcp_server):
    tools = mcp_server.list_tools()
    tool_names = [t["name"] for t in tools]
    assert "memory_retain" in tool_names
    assert "memory_recall" in tool_names
    assert "memory_reflect" in tool_names
    assert "deal_analytics" in tool_names
    assert "generate_dossier" in tool_names
    assert "stage_workspace" in tool_names
    assert "get_adaptive_recommendations" in tool_names
    assert "connect_mcp" in tool_names

    # Test tool execution over MCP interface
    call_res = mcp_server.handle_tool_call("memory_retain", {
        "namespace": "dias_deals",
        "key": "mcp_test_key",
        "data": {"content": "MCP Tool Test Inscription"}
    })
    assert call_res["status"] == "success"

    recall_res = mcp_server.handle_tool_call("memory_recall", {
        "namespace": "dias_deals",
        "query": "MCP Tool Test",
        "top_k": 2
    })
    assert recall_res["status"] == "success"
    assert len(recall_res["result"]) > 0
