import os
import json
from typing import List, Dict, Any, Optional
from src.telemetry_analyzer import TelemetryAnalyzer
from src.memory.hindsight_client import HindsightClient

class AdaptiveRouter:
    """
    Adaptive MCP Recommendation & Wiring Engine driven by Hindsight memory and reflection.
    Translates observed user interactions and telemetry into proactive MCP server recommendations.
    """
    def __init__(self, hindsight_client: Optional[HindsightClient] = None, telemetry_analyzer: Optional[TelemetryAnalyzer] = None):
        self.client = hindsight_client or HindsightClient()
        self.telemetry = telemetry_analyzer or TelemetryAnalyzer(self.client)
        self.connected_mcps: Dict[str, Dict[str, Any]] = {
            "hindsight_cloud": {
                "name": "Vectorize Hindsight Cloud",
                "role": "Cognitive Brain & Persistent Memory",
                "status": "connected",
                "transport": "cloud_sdk"
            }
        }

    def get_recommendations(self) -> List[Dict[str, Any]]:
        """
        Analyzes telemetry patterns and Hindsight reflections to generate proactive MCP recommendations.
        """
        analysis = self.telemetry.analyze_patterns()
        patterns = analysis.get("pattern_counts", {})
        recommendations = []

        # Rule 1: Database queries -> Neon PostgreSQL MCP
        if patterns.get("database_queries", 0) >= 3 and "neon_postgresql" not in self.connected_mcps:
            recommendations.append({
                "id": "neon_postgresql",
                "name": "Neon PostgreSQL MCP",
                "category": "Serverless Database & Schema Analytics",
                "trigger": f"Detected {patterns['database_queries']} database queries in interaction history.",
                "hindsight_justification": "Account frequently examines transactional schemas and deal pipeline tables.",
                "capabilities": ["Execute read-only queries", "Inspect schema trees", "Instant serverless DB branch isolation"],
                "impact_score": 95,
                "status": "recommended"
            })

        # Rule 2: Slack mentions -> Slack MCP
        if patterns.get("slack_mentions", 0) >= 2 and "slack" not in self.connected_mcps:
            recommendations.append({
                "id": "slack",
                "name": "Slack MCP",
                "category": "Team Collaboration & Deal Escalation",
                "trigger": f"Detected {patterns['slack_mentions']} Slack/messaging collaboration requests.",
                "hindsight_justification": "Deal momentum requires instant alerting to executive stakeholders on channel #sales-wins.",
                "capabilities": ["Post real-time deal alerts", "Create negotiation incident channels", "Notify account executive"],
                "impact_score": 88,
                "status": "recommended"
            })

        # Rule 3: Salesforce CPQ mentions -> Dynamic CPQ Battlecards
        if patterns.get("cpq_mentions", 0) >= 2 and "salesforce_cpq" not in self.connected_mcps:
            recommendations.append({
                "id": "salesforce_cpq",
                "name": "Salesforce CPQ Intelligence MCP",
                "category": "Enterprise Pricing & Quoting Governance",
                "trigger": f"Detected {patterns['cpq_mentions']} complex pricing or discount authorization queries.",
                "hindsight_justification": "Customer negotiation exhibits pricing friction; dynamic discount authority needed.",
                "capabilities": ["Calculate multi-tier volume discounts", "Validate margin guardrails", "Generate CPQ battlecards"],
                "impact_score": 90,
                "status": "recommended"
            })

        # Rule 4: Scheduling friction -> Google Calendar MCP
        if patterns.get("calendar_mentions", 0) >= 2 and "google_calendar" not in self.connected_mcps:
            recommendations.append({
                "id": "google_calendar",
                "name": "Google Calendar MCP",
                "category": "Executive Meeting & Schedule Management",
                "trigger": f"Detected {patterns['calendar_mentions']} scheduling and calendar hold interactions.",
                "hindsight_justification": "Frequent executive availability friction during enterprise closing cycles.",
                "capabilities": ["Stage tentative executive holds", "Detect time zone conflicts", "Send calendar invitations with human review"],
                "impact_score": 85,
                "status": "recommended"
            })

        # Default recommendation if early in the interaction cycle
        if not recommendations:
            recommendations.append({
                "id": "neon_postgresql",
                "name": "Neon PostgreSQL MCP",
                "category": "Serverless Database & Pipeline Analytics",
                "trigger": "Recommended for high-volume enterprise sales pipeline querying.",
                "hindsight_justification": "Standard baseline capability for relational deal data warehousing.",
                "capabilities": ["Live database schema inspection", "Cross-deal win/loss query aggregation"],
                "impact_score": 80,
                "status": "available"
            })

        return recommendations

    def connect_mcp(self, mcp_id: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Dynamically connects and wires the approved MCP server into the agent's active registry.
        """
        supported_profiles = {
            "neon_postgresql": {
                "name": "Neon PostgreSQL MCP",
                "transport": "stdio",
                "command": "npx -y @neondatabase/mcp-server",
                "capabilities": ["query", "describe_table", "branch"]
            },
            "slack": {
                "name": "Slack MCP",
                "transport": "sse",
                "command": "slack-mcp-server",
                "capabilities": ["post_message", "list_channels"]
            },
            "salesforce_cpq": {
                "name": "Salesforce CPQ Intelligence MCP",
                "transport": "python_module",
                "command": "src.narrative.battlecards",
                "capabilities": ["evaluate_discount", "generate_battlecard"]
            },
            "google_calendar": {
                "name": "Google Calendar MCP",
                "transport": "google_api",
                "command": "src.workspace.workspace_mcp",
                "capabilities": ["stage_meeting", "check_conflicts"]
            }
        }

        profile = supported_profiles.get(mcp_id, {
            "name": mcp_id,
            "transport": "stdio",
            "command": f"mcp-server-{mcp_id}",
            "capabilities": ["custom_tool"]
        })

        self.connected_mcps[mcp_id] = {
            "id": mcp_id,
            "name": profile["name"],
            "status": "connected",
            "transport": profile["transport"],
            "command": profile["command"],
            "capabilities": profile["capabilities"],
            "config": config or {}
        }

        # Retain adaptive wiring event into Hindsight memory
        self.client.retain(
            memory_bank_id="dias_telemetry",
            key=f"mcp_connection_{mcp_id}",
            data={
                "event_type": "mcp_adaptation",
                "mcp_connected": mcp_id,
                "rationale": "Adaptive recommendation approved by user/agent policy",
                "status": "active"
            },
            retention_policy="system_config"
        )

        return {
            "status": "connected",
            "mcp_id": mcp_id,
            "profile": self.connected_mcps[mcp_id]
        }
