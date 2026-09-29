from typing import List, Dict, Any, Optional

class DealScorer:
    """
    Multi-vector deal health scoring engine (1 to 100).
    Evaluates:
      1. Engagement Momentum (25%)
      2. Stakeholder Multi-Threading (25%)
      3. Technical Alignment & Compliance (25%)
      4. Commercial Feasibility & Budget (25%)
    """
    def __init__(self):
        pass

    def calculate_health(self, deal_data: Dict[str, Any], historical_memories: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Calculates holistic health score and win probability from current deal parameters and recalled memories.
        """
        history = historical_memories or []
        combined_text = " ".join([
            deal_data.get("notes", ""),
            deal_data.get("summary", ""),
            " ".join([m.get("content", "") for m in history if isinstance(m, dict)])
        ]).lower()

        # Vector 1: Engagement Momentum (0-25)
        last_contact_days = deal_data.get("last_contact_days", 3)
        interactions_count = deal_data.get("interaction_count", 5) + len(history)
        if last_contact_days <= 3 and interactions_count >= 4:
            momentum_score = 24.0
        elif last_contact_days <= 7:
            momentum_score = 19.0
        elif last_contact_days <= 14:
            momentum_score = 14.0
        else:
            momentum_score = 8.0

        # Vector 2: Stakeholder Multi-Threading (0-25)
        stakeholders = deal_data.get("stakeholders", [])
        roles = [s.get("role", "").lower() for s in stakeholders if isinstance(s, dict)]
        has_champion = any("champion" in r or "director" in r or "vp" in r for r in roles)
        has_economic_buyer = any("cfo" in r or "cro" in r or "finance" in r or "buyer" in r for r in roles)
        has_security_lead = any("security" in r or "ciso" in r or "it" in r or "compliance" in r for r in roles) or ("soc2" in combined_text or "okta" in combined_text)
        
        stakeholder_score = 10.0
        if has_champion:
            stakeholder_score += 6.0
        if has_economic_buyer:
            stakeholder_score += 5.0
        if has_security_lead:
            stakeholder_score += 4.0
        stakeholder_score = min(25.0, stakeholder_score)

        # Vector 3: Technical Alignment (0-25)
        technical_score = 18.0
        if any(w in combined_text for w in ["govcloud", "okta", "sso", "soc2", "gdpr", "api"]):
            technical_score += 4.0
        if "blocker" in combined_text or "unsupported" in combined_text:
            technical_score -= 8.0
        technical_score = max(5.0, min(25.0, technical_score))

        # Vector 4: Commercial Feasibility (0-25)
        commercial_score = 17.0
        if any(w in combined_text for w in ["budget approved", "allocated", "approved pricing"]):
            commercial_score += 6.0
        elif any(w in combined_text for w in ["discount", "too expensive", "procurement review"]):
            commercial_score += 2.0
        commercial_score = min(25.0, commercial_score)

        total_health = round(momentum_score + stakeholder_score + technical_score + commercial_score, 1)
        win_probability = round(min(95.0, max(15.0, total_health * 0.92)), 1)

        # Classify health band
        if total_health >= 80:
            health_tier = "EXCELLENT"
            color_hex = "#16A34A"
        elif total_health >= 65:
            health_tier = "HEALTHY"
            color_hex = "#2563EB"
        elif total_health >= 50:
            health_tier = "AT RISK"
            color_hex = "#D97706"
        else:
            health_tier = "CRITICAL"
            color_hex = "#DC2626"

        risks = []
        if not has_economic_buyer:
            risks.append("Economic Buyer (CFO/CRO) not yet multi-threaded in negotiations.")
        if "competitor" in combined_text or "gong" in combined_text or "clari" in combined_text:
            risks.append("Active bake-off with competitor requires differentiation battlecards.")
        if "discount" in combined_text:
            risks.append("Procurement requesting discount concession; margin safeguard required.")

        opportunities = [
            "Executive sponsor highly engaged with positive product feedback.",
            "Technical compliance requirements (SOC2, Okta SSO) are well-aligned with product capabilities.",
            "Fast-track procurement possible if mutual close plan is staged."
        ]

        return {
            "overall_health_score": total_health,
            "win_probability_pct": win_probability,
            "health_tier": health_tier,
            "color_hex": color_hex,
            "vectors": {
                "momentum": {"score": momentum_score, "max": 25.0},
                "stakeholders": {"score": stakeholder_score, "max": 25.0, "coverage_count": len(stakeholders)},
                "technical_alignment": {"score": technical_score, "max": 25.0},
                "commercial_feasibility": {"score": commercial_score, "max": 25.0}
            },
            "risk_factors": risks,
            "growth_opportunities": opportunities,
            "next_recommended_action": "Execute executive follow-up with customized compliance dossier and stage procurement review session."
        }
