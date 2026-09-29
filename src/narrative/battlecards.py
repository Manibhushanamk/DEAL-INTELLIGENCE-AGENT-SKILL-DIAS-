from typing import Dict, Any, List, Optional

class BattlecardEngine:
    """
    Competitive battlecard and objection handling generator for enterprise B2B sales.
    Specializes in positioning against Gong, Clari, and Salesforce CPQ with compliance strengths.
    """
    def __init__(self):
        self._battlecards = {
            "gong": {
                "competitor_name": "Gong.io",
                "core_weakness": "High per-seat pricing, shallow pipeline risk modeling, no native coding agent skill integration.",
                "our_advantage": "Autonomous AI agent architecture with Vectorize Hindsight persistent memory, multi-vector deal health scoring, and adaptive MCP tool execution.",
                "trap_question": "Does their conversation intelligence retain long-term memory across engineering, security, and procurement meetings, or just call recording transcripts?",
                "landmines_to_lay": ["Per-seat renewal spikes", "Lack of serverless schema branching (Neon)", "Black-box proprietary models"]
            },
            "clari": {
                "competitor_name": "Clari",
                "core_weakness": "Rigid top-down forecasting grids, slow data synchronization, heavy manual CRM hygiene burden on reps.",
                "our_advantage": "Continuous self-learning agent loop that automatically extracts deal disclosures into Hindsight Cloud and stages actions with zero manual data entry.",
                "trap_question": "How many hours per week do sales reps spend updating CRM fields instead of the system dynamically retaining and reflecting deal changes?",
                "landmines_to_lay": ["Complex 6-month deployment cycles", "High administrative overhead", "Rigid forecasting formulas"]
            },
            "salesforce_cpq": {
                "competitor_name": "Salesforce CPQ",
                "core_weakness": "Legacy architecture, slow quote generation latency, brittle rule tables.",
                "our_advantage": "Instant AI agent-driven discount validation, margin guardrail simulation, and adaptive quote structuring.",
                "trap_question": "Can your reps generate custom compliant multi-tier pricing in seconds with automated compliance audit trails?",
                "landmines_to_lay": ["Months of specialized consultant configuration", "Slow loading quote engines"]
            }
        }

    def get_battlecard(self, competitor_name: str) -> Dict[str, Any]:
        """Returns competitive battlecard for given competitor."""
        key = competitor_name.lower().replace(" ", "_")
        for k, card in self._battlecards.items():
            if k in key:
                return card
        return {
            "competitor_name": competitor_name,
            "core_weakness": "Generic legacy CRM tool without adaptive agent skill integration or long-term cognitive memory.",
            "our_advantage": "Self-configuring Hindsight Cloud memory that learns buyer patterns day-by-day and adapts MCP tools.",
            "trap_question": "Does your solution adapt its tools dynamically as the deal negotiation evolves?",
            "landmines_to_lay": ["High switching costs", "Lack of autonomous memory", "Vendor lock-in"]
        }

    def generate_objection_response(self, objection_category: str, client_context: Optional[str] = None) -> Dict[str, Any]:
        """
        Generates tactical counter-narratives for commercial and technical objections.
        """
        cat = objection_category.lower()
        if "budget" in cat or "price" in cat or "discount" in cat:
            return {
                "category": "Commercial & Pricing",
                "objection": "Your solution is higher than the budgeted threshold.",
                "counter_narrative": "Offer phased rollout: Anchor year 1 on core deal intelligence with guaranteed ROI benchmarks. Frame cost against deal slippage and lost revenue prevented.",
                "tactical_action": "Propose tiered deployment: 100 enterprise licenses now with option to expand post-Q4 validation."
            }
        elif "security" in cat or "compliance" in cat or "govcloud" in cat or "sso" in cat:
            return {
                "category": "Technical & Security Compliance",
                "objection": "Security demands strict AWS GovCloud hosting, SOC2 Type II audit report, and Okta SAML 2.0 SSO.",
                "counter_narrative": "Lead with full SOC2 Type II certification, tenant data isolation in Neon/PostgreSQL, and turnkey Okta SAML integration.",
                "tactical_action": "Attach the C-level Executive Security Dossier directly to the procurement response."
            }
        else:
            return {
                "category": "General Adoption",
                "objection": "We already have standard CRM reporting.",
                "counter_narrative": "Standard CRM shows what happened in the past; DIAS with Hindsight memory tells you what to do next to win the deal.",
                "tactical_action": "Run side-by-side deal analysis on an active high-stakes account."
            }
