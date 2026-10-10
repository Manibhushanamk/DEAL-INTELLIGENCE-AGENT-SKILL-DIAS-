---
name: dias
description: Deal Intelligence Agent Skill (DIAS) — An autonomous sales intelligence copilot that remembers deal context using Vectorize Hindsight Cloud, stores structured records in Neon PostgreSQL, integrates with Google Workspace (Gmail, Calendar, Docs, Sheets), and executes the /dias and /dias-input-end command lifecycle.
---

# Deal Intelligence Agent Skill (DIAS)

DIAS transforms AI coding and CLI agents (Google Antigravity, Claude Code, Cursor, OpenClaw, Jules) into an autonomous enterprise sales intelligence copilot.

---

## 1. When to Use This Skill

Invoke this skill whenever:
- The user runs `/dias` or `/dias-input-end`.
- The user provides meeting transcripts, call notes, RFPs, or deal summaries for enterprise software deals.
- The user wants deal health scoring, risk analysis, competitive battlecards (e.g., vs Gong, Clari, Salesforce).
- The user needs Google Workspace artifacts (executive Google Doc dossier, Master Deal Tracker Google Sheet sync, Gmail follow-up drafts, Google Calendar holds).
- The user requires persistent memory across sessions via Vectorize Hindsight Cloud and Neon PostgreSQL.

---

## 2. Command Flow & Lifecycle

The skill operates through two core commands:

```
[User invokes /dias] ──> [Audit Integrations & OAuth] ──> [Collect Notes & Q&A]
                                                                  │
                                                                  ▼
[User invokes /dias-input-end] ──> [Score Deal] ──> [Google Workspace & PDF] ──> [Neon & Hindsight]
```

### Command 1: `/dias` (Start / Resume Session)

When the user enters `/dias` or provides initial deal notes:

1. **Verify Integrations & Google OAuth**:
   - Check if Google Workspace OAuth is authorized.
   - If not yet authorized, launch the OAuth flow:
     ```bash
     python3 dias_cli.py /oauth
     ```
     This opens the Google sign-in consent browser for Gmail, Calendar, Docs, Sheets, and Drive scopes.
   - Neon PostgreSQL and Vectorize Hindsight Cloud are pre-configured with embedded fallbacks and require no extra setup.

2. **Ingest Deal Context**:
   - Ingest user input, pasted notes, emails, transcripts, or deal IDs.
   - Execute:
     ```bash
     python3 dias_cli.py /dias --input "<user_input_or_notes>"
     ```
   - DIAS normalizes the deal profile and classifies information into:
     - **Verified Facts**: Confirmed budget approval, signed terms, hard technical requirements (SOC2, Okta, GovCloud).
     - **User Claims**: Unverified client statements.
     - **Assumptions**: Inferred timeline or sizing.
     - **Unknowns**: Crucial missing fields (e.g., Economic Buyer, Target Close Date).

3. **Targeted Discovery Questions**:
   - Present the current deal profile to the user.
   - Ask only high-leverage questions to resolve essential unknowns (e.g., "Who is the Economic Buyer / CFO?" or "What is the targeted close date?").

---

### Command 2: `/dias-input-end` (Analyze & Deliver)

When the user enters `/dias-input-end` or states they are done providing input:

1. **Execute Analysis & Delivery Pipeline**:
   - Run:
     ```bash
     python3 dias_cli.py /dias-input-end
     ```
2. **What DIAS Executes Automatically**:
   - **Validation**: Checks deal sanity and essential fields.
   - **Memory Recall**: Surfaces historical patterns from **Vectorize Hindsight Cloud** (`dias_deals`).
   - **Multi-Vector Deal Scoring**: Computes 100-point Health Score and win probability % based on Engagement Momentum (25%), Stakeholder Depth (25%), Technical Alignment (25%), and Commercial Feasibility (25%).
   - **C-Level Executive Dossier**:
     - Generates publication-grade **ReportLab PDF** in `reports/`.
     - Creates formatted 12-section **Google Doc** with executive summaries and battlecards.
   - **Master Deal Tracker Google Sheet**: Auto-creates or appends to the master spreadsheet with deal metrics and direct doc links.
   - **Workspace Collateral Staging**:
     - Creates **Gmail follow-up draft** (outbound sending is strictly safety-gated).
     - Schedules **Google Calendar hold** with collision detection.
   - **Authoritative Persistence**: Commits all structured records to **Neon PostgreSQL** across 8 relational tables (`deals`, `stakeholders`, `deal_interactions`, `deal_risks`, `deal_assessments`, `deal_actions`, `dias_sessions`, `deal_documents`).
   - **Cognitive Retention**: Saves deal takeaways to **Vectorize Hindsight Cloud**.
3. **Present Results**:
   - Display executive summary, health scores, links to generated Google Doc/Sheet, PDF location, and recommended next steps.

---

## 3. Direct Python Controller Usage

Agents can also invoke the session controller directly in Python:

```python
from src.session.controller import DiasSessionController

controller = DiasSessionController()

# Step 1: Initialize and input notes
init_res = controller.handle_dias_command(
    user_input="We have a $350k deal with Acme Corp in Security Review. Competitor is Gong. VP of Security requires AWS GovCloud and Okta SSO. Close date is Nov 30, 2026."
)
print("Deal Profile:", init_res["deal_profile"])
print("Suggested Questions:", init_res["validation"]["suggested_questions"])

# Step 2: Conclude input and generate deliverables
result = controller.handle_dias_input_end_command()
print("Executive Summary:", result["executive_summary"])
print("Deliverables:", result["deliverables"])
```

---

## 4. Environment & Integration Details

- **Cognitive Brain**: Vectorize Hindsight Cloud (`api.hindsight.vectorize.io`, banks `dias_deals` and `dias_telemetry`).
- **Structured Database**: Neon Serverless PostgreSQL (8 tables, IPv4 pooler optimized).
- **Google Workspace**: Google Desktop OAuth 2.0 (`client_secret.json` bundled in repository).
- **Executive Dossier**: ReportLab PDF Engine (`reports/`).
