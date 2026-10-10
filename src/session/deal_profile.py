import re
import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone


class NormalizedDealProfile:
    """
    Maintains a normalized, structured deal profile:
    - Customer & Deal ID
    - Owner, Value & Currency
    - Stage & Budget Status
    - Stakeholders & Buying Authorities
    - Technical Requirements & Compliance
    - Competition & Objections
    - Risk Register & Mitigations
    - Important Dates & Milestones
    - Recommended Next Actions
    - Source References & Verification Matrix (Facts, Claims, Assumptions, Unknowns)
    """

    def __init__(self, deal_id: Optional[str] = None):
        self.deal_id = deal_id or f"DEAL-{int(datetime.now().timestamp())}"
        self.customer: str = "Unknown Enterprise"
        self.owner: str = "Account Executive"
        self.value: float = 0.0
        self.currency: str = "USD"
        self.stage: str = "Discovery"
        self.budget_status: str = "Unknown"
        self.competition: List[str] = []
        self.stakeholders: List[Dict[str, Any]] = []
        self.requirements: List[str] = []
        self.risks: List[Dict[str, Any]] = []
        self.important_dates: Dict[str, str] = {}
        self.next_actions: List[Dict[str, Any]] = []
        self.source_references: List[Dict[str, Any]] = []

        # Epistemic calibration: Fact vs Claim vs Assumption vs Unknown
        self.verified_facts: List[str] = []
        self.user_claims: List[str] = []
        self.assumptions: List[str] = []
        self.unknowns: List[str] = [
            "Customer name",
            "Contract value",
            "Economic buyer identity",
            "Budget allocation status",
            "Target close date",
            "Mandatory security requirements"
        ]

    def ingest_text(self, text: str, source: str = "user_notes") -> Dict[str, Any]:
        """Extracts structured deal facts, claims, and requirements from unstructured text."""
        if not text.strip():
            return {}

        self.source_references.append({
            "source": source,
            "snippet": text[:200] + ("..." if len(text) > 200 else ""),
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

        lower = text.lower()

        # 1. Deal ID extraction
        id_match = re.search(r'\b(DEAL-[A-Z0-9_-]+)\b', text, re.IGNORECASE)
        if id_match:
            self.deal_id = id_match.group(1).upper()

        # 2. Customer name extraction
        cust_match = re.search(r'(?:with|customer|client|company|account)\s+([A-Z][A-Za-z0-9&]+(?:\s+[A-Z][A-Za-z0-9&]+)?)', text)
        if cust_match:
            potential_name = cust_match.group(1).strip()
            if potential_name.lower() not in ["the", "a", "an", "our", "all"]:
                self.customer = potential_name
                self._resolve_unknown("Customer name")
                self.verified_facts.append(f"Customer identified as {self.customer}")
        elif "acme" in lower and self.customer == "Unknown Enterprise":
            self.customer = "Acme Corp"
            self._resolve_unknown("Customer name")
            self.verified_facts.append("Customer identified as Acme Corp")

        # 3. Contract value extraction
        val_match = re.search(r'[\$€£]\s*([0-9,]+(?:\.[0-9]+)?)\s*([kmbKMB]|thousand|million)?', text, re.IGNORECASE)
        if val_match:
            try:
                base_val = float(val_match.group(1).replace(',', ''))
                mult = (val_match.group(2) or '').lower()
                if mult.startswith('k') or mult == 'thousand':
                    base_val *= 1000
                elif mult.startswith('m') or mult == 'million':
                    base_val *= 1000000
                self.value = base_val
                self._resolve_unknown("Contract value")
                self.verified_facts.append(f"Contract value established at ${self.value:,.2f} {self.currency}")
            except Exception:
                pass

        # 4. Stage determination
        if any(w in lower for w in ["closed won", "contract signed"]):
            self.stage = "Closed Won"
        elif any(w in lower for w in ["procurement", "legal review", "negotiating"]):
            self.stage = "Negotiation / Procurement"
        elif any(w in lower for w in ["security review", "soc2", "compliance"]):
            self.stage = "Security & Compliance Review"
        elif any(w in lower for w in ["demo", "poc", "evaluation"]):
            self.stage = "Technical Evaluation / POC"

        # 5. Budget status
        if any(w in lower for w in ["budget approved", "budget allocated", "funds secured"]):
            self.budget_status = "Approved"
            self._resolve_unknown("Budget allocation status")
            self.verified_facts.append("Budget formally approved by client")
        elif "budget under review" in lower or "pending budget" in lower:
            self.budget_status = "Under Review"
            self.user_claims.append("Client states budget is under review")

        # 6. Competition & Incumbents
        for comp in ["gong", "clari", "salesforce", "hubspot", "outreach", "chorus"]:
            if comp in lower and comp.title() not in self.competition:
                self.competition.append(comp.title())
                self.verified_facts.append(f"Competitive bake-off active against {comp.title()}")

        # 7. Stakeholders
        if "cfo" in lower or "chief financial officer" in lower:
            self._add_stakeholder("CFO", "Economic Buyer", "High", "Needs ROI validation")
            self._resolve_unknown("Economic buyer identity")
        if "ciso" in lower or "vp of security" in lower or "security lead" in lower:
            self._add_stakeholder("VP of Security", "Security Gatekeeper", "High", "Mandatory SOC2/Okta requirements")
        if "champion" in lower or "vp of engineering" in lower or "director" in lower:
            self._add_stakeholder("VP of Engineering", "Internal Champion", "High", "Strong advocate for architecture")

        # 8. Technical requirements
        tech_keywords = [
            ("aws govcloud", "AWS GovCloud Deployment"),
            ("okta", "Okta SSO SAML 2.0 Integration"),
            ("soc2", "SOC2 Type II Audit Report"),
            ("sso", "Single Sign-On (SSO) Support"),
            ("api", "REST / GraphQL API Access"),
            ("gdpr", "GDPR Data Processing Agreement")
        ]
        for kw, req_desc in tech_keywords:
            if kw in lower and req_desc not in self.requirements:
                self.requirements.append(req_desc)
                self._resolve_unknown("Mandatory security requirements")
                self.verified_facts.append(f"Client requirement: {req_desc}")

        # 9. Important dates
        date_match = re.search(r'(?:close|deadline|target|timeline)\s*[:=-]?\s*([A-Za-z0-9\s,]{4,25})', text)
        if date_match:
            date_str = date_match.group(1).strip()
            date_str = re.sub(r'^(is|by|at|in|on)\s+', '', date_str, flags=re.IGNORECASE).strip()
            self.important_dates["Target Close"] = date_str
            self._resolve_unknown("Target close date")
        elif "q4" in lower:
            self.important_dates["Target Close"] = "End of Q4 2026"
            self._resolve_unknown("Target close date")

        # 10. Risks
        if "objection" in lower or "too expensive" in lower or "discount" in lower:
            self.risks.append({
                "risk_type": "Commercial",
                "description": "Procurement requesting discount concession",
                "severity": "Medium",
                "mitigation": "Highlight persistent memory ROI and lower total cost of ownership (TCO)"
            })
        if "blocker" in lower or "govcloud" in lower:
            self.risks.append({
                "risk_type": "Technical / Compliance",
                "description": "Mandatory GovCloud and SOC2 compliance sign-off required",
                "severity": "High",
                "mitigation": "Supply security architecture whitepaper and SOC2 bridge letter"
            })

        return self.to_dict()

    def _add_stakeholder(self, name_or_role: str, title: str, authority: str, note: str) -> None:
        if not any(s["title"] == title for s in self.stakeholders):
            self.stakeholders.append({
                "name": name_or_role,
                "role": title,
                "title": title,
                "email": f"{name_or_role.lower().replace(' ', '.')}@client.com",
                "buying_authority": authority,
                "note": note
            })

    def _resolve_unknown(self, item: str) -> None:
        if item in self.unknowns:
            self.unknowns.remove(item)

    def ingest_file(self, file_path: str) -> Dict[str, Any]:
        """Reads and ingests text, json, or markdown file."""
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            return self.ingest_text(content, source=f"file:{os.path.basename(file_path)}")
        except Exception as e:
            return {"error": f"Failed to read file: {str(e)}"}

    def validate_inputs(self) -> Dict[str, Any]:
        """Validates completeness, flags conflicts, and identifies essential missing fields."""
        missing = []
        conflicts = []

        if self.customer == "Unknown Enterprise":
            missing.append("Customer/Account name")
        if self.value <= 0:
            missing.append("Deal value / ACV")
        if not self.stakeholders:
            missing.append("Key stakeholders or economic buyer")
        if not self.important_dates.get("Target Close"):
            missing.append("Expected closing timeline / target date")

        # Conflict checks
        if self.stage == "Closed Won" and self.budget_status == "Under Review":
            conflicts.append("Deal marked Closed Won but budget is still under review.")

        return {
            "is_valid": len(missing) == 0,
            "completeness_score_pct": max(20, int(100 - (len(missing) * 20))),
            "missing_essential_fields": missing,
            "conflicts_detected": conflicts,
            "unknowns": self.unknowns,
            "targeted_clarification_questions": self._generate_clarification_questions(missing)
        }

    def _generate_clarification_questions(self, missing: List[str]) -> List[str]:
        questions = []
        if "Customer/Account name" in missing:
            questions.append("What is the name of the prospective enterprise customer?")
        if "Deal value / ACV" in missing:
            questions.append("What is the anticipated Annual Contract Value (ACV) or budget range for this deal?")
        if "Key stakeholders or economic buyer" in missing:
            questions.append("Who is the primary economic buyer or executive sponsor involved in this decision?")
        if "Expected closing timeline / target date" in missing:
            questions.append("What is the target closing date or fiscal quarter for contract execution?")
        return questions

    def to_dict(self) -> Dict[str, Any]:
        return {
            "deal_id": self.deal_id,
            "customer": self.customer,
            "owner": self.owner,
            "value": self.value,
            "currency": self.currency,
            "stage": self.stage,
            "budget_status": self.budget_status,
            "competition": ", ".join(self.competition) if self.competition else "None",
            "stakeholders": self.stakeholders,
            "requirements": self.requirements,
            "risks": self.risks,
            "important_dates": self.important_dates,
            "timeline": self.important_dates.get("Target Close", "Q4 2026"),
            "next_actions": self.next_actions,
            "verified_facts": self.verified_facts,
            "user_claims": self.user_claims,
            "assumptions": self.assumptions,
            "unknowns": self.unknowns
        }
