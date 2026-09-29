import os
import pytest
from src.core_skill import DealIntelligenceSkill

def test_dossier_compilation(tmp_path):
    # Use mock key to avoid slow network timeouts during PDF compilation test
    skill = DealIntelligenceSkill(api_key="mock_test_key")
    pdf_path = str(tmp_path / "test_acme_dossier.pdf")

    deal_data = {
        "deal_id": "DEAL-ACME-001",
        "customer": "Acme Corp",
        "amount": "$350,000",
        "close_date": "Q4 2026",
        "competitor": "Gong.io",
        "stage": "Negotiation",
        "last_contact_days": 2,
        "interaction_count": 6,
        "stakeholders": [
            {"name": "Sarah Chen", "role": "VP of Security"},
            {"name": "Mark Roberts", "role": "Director of Sales Ops (Champion)"}
        ],
        "notes": "Acme Corp evaluated Gong and Clari. Mandated AWS GovCloud deployment, Okta SSO, and SOC2 compliance."
    }

    out_file = skill.generate_dossier(pdf_path, "Acme Corp", deal_data)
    assert os.path.exists(out_file)
    assert os.path.getsize(out_file) > 3000
