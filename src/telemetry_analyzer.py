from typing import List, Dict, Any, Optional
from collections import Counter
from datetime import datetime, timezone
from src.memory.hindsight_client import HindsightClient

class TelemetryAnalyzer:
    """
    Day-by-day telemetry logging, learning analysis, and reflection workflow.
    Tracks user queries, tool invocations, friction points, and feeds them into Hindsight Cloud (Domain 2).
    """
    def __init__(self, hindsight_client: Optional[HindsightClient] = None):
        self.client = hindsight_client or HindsightClient()
        self.telemetry_bank = "dias_telemetry"
        self._local_events: List[Dict[str, Any]] = []

    def record_interaction(
        self,
        query: str,
        tool_invoked: Optional[str] = None,
        context: Optional[str] = None,
        interaction_day: int = 1
    ) -> Dict[str, Any]:
        """
        Records a user interaction or tool execution into Hindsight Telemetry bank.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        event = {
            "query": query,
            "tool_invoked": tool_invoked or "general_query",
            "context": context or "sales_intelligence",
            "interaction_day": interaction_day,
            "timestamp": timestamp
        }
        self._local_events.append(event)

        # Retain into Hindsight Cloud telemetry namespace
        key = f"telemetry_{interaction_day}_{len(self._local_events)}"
        self.client.retain(
            memory_bank_id=self.telemetry_bank,
            key=key,
            data=event,
            retention_policy="telemetry_log"
        )
        return {"status": "recorded", "event_key": key}

    def analyze_patterns(self) -> Dict[str, Any]:
        """
        Analyzes logged interactions for workflow friction and repeated intents.
        Feeds results into Hindsight reflection.
        """
        all_events = self._local_events
        # Also recall recent telemetry from Hindsight
        cloud_events = self.client.recall(
            memory_bank_id=self.telemetry_bank,
            query="telemetry interaction query friction",
            top_k=25
        )
        combined = all_events + [e for e in cloud_events if isinstance(e, dict) and e not in all_events]

        queries = [e.get("query", "").lower() for e in combined]
        tools = [e.get("tool_invoked", "") for e in combined]

        # Pattern indicators
        db_mentions = sum(1 for q in queries if any(w in q for w in ["database", "postgres", "sql", "schema", "table", "query"]))
        slack_mentions = sum(1 for q in queries if any(w in q for w in ["slack", "channel", "alert", "ping team"]))
        cpq_mentions = sum(1 for q in queries if any(w in q for w in ["salesforce", "cpq", "quote", "discount approval"]))
        calendar_mentions = sum(1 for q in queries if any(w in q for w in ["calendar", "schedule", "meeting", "conflict", "hold time"]))

        # Friction flags
        friction_flags = []
        if db_mentions >= 3:
            friction_flags.append({
                "type": "database_friction",
                "count": db_mentions,
                "message": f"Detected {db_mentions} database/SQL queries. Direct DB access would accelerate workflow."
            })
        if slack_mentions >= 2:
            friction_flags.append({
                "type": "slack_collaboration_friction",
                "count": slack_mentions,
                "message": f"Detected {slack_mentions} Slack/messaging requests. Team notifications should be automated."
            })
        if cpq_mentions >= 2:
            friction_flags.append({
                "type": "cpq_pricing_friction",
                "count": cpq_mentions,
                "message": f"Detected {cpq_mentions} enterprise pricing/CPQ queries. Dynamic battlecards recommended."
            })
        if calendar_mentions >= 2:
            friction_flags.append({
                "type": "calendar_friction",
                "count": calendar_mentions,
                "message": f"Detected {calendar_mentions} scheduling interactions. Google Calendar staging recommended."
            })

        # Run reflection over telemetry
        reflection = self.client.reflect(
            memory_bank_id=self.telemetry_bank,
            topic="agent_tool_friction_and_mcp_adaptation"
        )

        return {
            "total_events_logged": len(combined),
            "tool_distribution": dict(Counter(tools)),
            "pattern_counts": {
                "database_queries": db_mentions,
                "slack_mentions": slack_mentions,
                "cpq_mentions": cpq_mentions,
                "calendar_mentions": calendar_mentions
            },
            "friction_flags": friction_flags,
            "hindsight_reflection": reflection
        }
