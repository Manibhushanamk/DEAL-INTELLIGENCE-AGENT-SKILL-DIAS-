import os
import json
import argparse
from typing import Dict, Any, List, Optional
from src.memory.hindsight_client import HindsightClient
from src.analytics.deal_scorer import DealScorer
from src.narrative.battlecards import BattlecardEngine
from src.workspace.workspace_mcp import WorkspaceManager
from src.dossier.pdf_generator import PDFDossierGenerator
from src.telemetry_analyzer import TelemetryAnalyzer
from mcp.adaptive_router import AdaptiveRouter

class DealIntelligenceSkill:
    """
    Unified controller and cognitive engine for Deal Intelligence Agent Skill (DIAS).
    Coordinates Hindsight Cloud persistent memory, multi-vector deal health scoring,
    executive PDF compilation, workspace action staging, and adaptive MCP routing.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.memory = HindsightClient(api_key=api_key)
        self.scorer = DealScorer()
        self.battlecards = BattlecardEngine()
        self.workspace = WorkspaceManager()
        self.dossier = PDFDossierGenerator()
        self.telemetry = TelemetryAnalyzer(self.memory)
        self.router = AdaptiveRouter(self.memory, self.telemetry)

    # 1. Cognitive Memory Operations (Hindsight Cloud)
    def memory_retain(self, namespace: str = "dias_deals", key: str = "deal_fact", data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Inscribes deal facts, customer disclosures, or telemetry into Hindsight Cloud."""
        self.telemetry.record_interaction(query=f"retain memory {key}", tool_invoked="memory_retain")
        return self.memory.retain(namespace=namespace, key=key, data=data or {})

    def memory_recall(self, namespace: str = "dias_deals", query: str = "", top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieves semantically relevant historical memories from Hindsight Cloud."""
        self.telemetry.record_interaction(query=f"recall query: {query}", tool_invoked="memory_recall")
        return self.memory.recall(namespace=namespace, query=query, top_k=top_k)

    def memory_reflect(self, namespace: str = "dias_deals", topic: str = "deal_strategy") -> Dict[str, Any]:
        """Synthesizes high-order strategic beliefs, patterns, and risks across memories."""
        self.telemetry.record_interaction(query=f"reflect on topic: {topic}", tool_invoked="memory_reflect")
        return self.memory.reflect(namespace=namespace, topic=topic)

    # 2. Multi-Vector Deal Analytics
    def deal_analytics(self, deal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculates multi-vector health score (1-100), win probability, and diagnostic radar."""
        deal_id = deal_data.get("deal_id", "DEAL-001")
        # Recall relevant memories for this deal
        history = self.memory.recall(namespace="dias_deals", query=f"{deal_id} {deal_data.get('customer', '')}", top_k=5)
        analytics = self.scorer.calculate_health(deal_data, historical_memories=history)
        self.telemetry.record_interaction(query=f"deal analytics for {deal_id}", tool_invoked="deal_analytics")
        return analytics

    # 3. Executive Dossier Generation
    def generate_dossier(self, output_filepath: str, account_name: str, deal_data: Dict[str, Any]) -> str:
        """Compiles a C-level executive PDF deal dossier using ReportLab."""
        analytics = self.deal_analytics(deal_data)
        competitor = deal_data.get("competitor", "Gong")
        battlecard = self.battlecards.get_battlecard(competitor)
        reflection = self.memory.reflect(namespace="dias_deals", topic=account_name)
        beliefs = reflection.get("consolidated_beliefs", [])

        path = self.dossier.generate_dossier(
            output_filepath=output_filepath,
            account_name=account_name,
            deal_data=deal_data,
            analytics_summary=analytics,
            battlecard=battlecard,
            hindsight_reflections=beliefs
        )
        self.telemetry.record_interaction(query=f"generate dossier for {account_name}", tool_invoked="generate_dossier")
        return path

    # 4. Workspace Action Staging (Human-in-the-Loop)
    def stage_workspace(self, action_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Safely stages Gmail follow-up drafts or Calendar invitations with human review."""
        if action_type == "email":
            action = self.workspace.stage_followup_email(
                recipient_email=params.get("recipient", "champion@acme.com"),
                subject=params.get("subject", "Executive Deal Follow-up"),
                body_text=params.get("body", "Attached please find the executive dossier."),
                deal_id=params.get("deal_id", "DEAL-001")
            )
        elif action_type == "calendar":
            action = self.workspace.stage_calendar_hold(
                meeting_title=params.get("title", "Procurement Alignment"),
                attendees=params.get("attendees", ["buyer@acme.com"]),
                duration_minutes=params.get("duration", 30),
                proposed_time=params.get("time", "Tuesday 2:00 PM EST"),
                deal_id=params.get("deal_id", "DEAL-001")
            )
        else:
            action = {"status": "error", "message": f"Unsupported action type: {action_type}"}

        self.telemetry.record_interaction(query=f"stage workspace action {action_type}", tool_invoked="stage_workspace")
        return action

    # 5. Adaptive MCP Routing
    def get_adaptive_recommendations(self) -> List[Dict[str, Any]]:
        """Evaluates interaction history and Hindsight reflections to recommend high-impact MCP servers."""
        return self.router.get_recommendations()

    def connect_mcp(self, mcp_id: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Dynamically connects approved MCP servers into the active agent registry."""
        return self.router.connect_mcp(mcp_id, config)

def main():
    parser = argparse.ArgumentParser(description="Deal Intelligence Agent Skill Core Entrypoint")
    parser.add_argument("--health-check", action="store_true", help="Run pre-flight triad health check")
    parser.add_argument("--demo", action="store_true", help="Run the full 3-minute Acme Corp demo flow")
    args = parser.parse_args()

    skill = DealIntelligenceSkill()
    if args.health_check:
        res = skill.memory.execute_preflight_triad()
        print(json.dumps(res, indent=2))
    elif args.demo:
        print("[DIAS] Running Acme Corp demonstration flow...")
        # 1. Retain Acme Corp initial deal context
        skill.memory_retain(
            key="acme_corp_meeting_1",
            data={
                "deal_id": "DEAL-ACME-001",
                "customer": "Acme Corp",
                "content": "Acme Corp evaluated Gong and Clari. Mandated AWS GovCloud deployment, Okta SSO, and SOC2 compliance."
            }
        )
        # 2. Recall memory
        recalled = skill.memory_recall(query="What compliance does Acme require?", top_k=2)
        print(f"[Hindsight Recall] Recalled {len(recalled)} memories.")
        # 3. Deal health score
        deal_data = {
            "deal_id": "DEAL-ACME-001",
            "customer": "Acme Corp",
            "amount": "$350,000",
            "close_date": "Q4 2026",
            "competitor": "Gong.io",
            "last_contact_days": 2,
            "interaction_count": 6,
            "stakeholders": [
                {"name": "Sarah Chen", "role": "VP of Security"},
                {"name": "Mark Roberts", "role": "Director of Sales Ops (Champion)"}
            ]
        }
        score = skill.deal_analytics(deal_data)
        print(f"[Deal Analytics] Health Score: {score['overall_health_score']}/100, Win Prob: {score['win_probability_pct']}%")
        # 4. Generate Dossier
        dossier_path = skill.generate_dossier("/home/kmanib/deal-intelligence-skill/acme_corp_deal_dossier.pdf", "Acme Corp", deal_data)
        print(f"[Executive Dossier] Generated PDF: {dossier_path}")
        # 5. Adaptive MCP
        recs = skill.get_adaptive_recommendations()
        print(f"[Adaptive MCP] Recommendations: {[r['name'] for r in recs]}")

if __name__ == "__main__":
    main()
