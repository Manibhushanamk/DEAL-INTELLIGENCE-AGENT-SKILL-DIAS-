---
name: deal-intelligence-skill
description: Self-configuring, Hindsight-powered cognitive skill that equips AI coding agents with long-term memory, multi-vector deal intelligence, adaptive MCP wiring, and executive PDF dossier generation.
version: 1.0.0
author: HackwithHyderabad 3.0 Finale Team
license: MIT
---

# Deal Intelligence Agent Skill (DIAS)

> **Central Architectural Principle:**  
> DIAS is a self-configuring, Hindsight-powered agent skill that establishes persistent memory during first-run installation, continuously retains and recalls deal and user context, reflects on accumulated interactions to learn patterns, and dynamically adapts its MCP capabilities as the user's workflow evolves.  
> **Vectorize Hindsight Cloud is the Cognitive Brain and Central Memory Layer.**

---

## 1. When to Invoke This Skill

Invoke this skill whenever:
- Working on B2B sales deals, enterprise client negotiations, procurement analysis, or revenue operations.
- The user or host agent needs **persistent memory** across developer sessions, remembering past architectural decisions, buyer objections, or project context.
- Assessing deal health, calculating win probabilities, or evaluating buyer objections (budget, security, SSO, compliance, competitive bake-offs).
- Compiling C-level executive PDF deal dossiers.
- Staging collaborative sales actions in Google Workspace (Gmail follow-ups, Calendar scheduling) with explicit human confirmation.
- Learning user workflow patterns over time and dynamically recommending or connecting MCP servers (e.g. Neon PostgreSQL, Slack, Google Calendar).

---

## 2. Host Agent Auto-Detection & Installation Flow

When installed, DIAS follows an 8-step Hindsight-first configuration protocol:

1. **Host Agent Auto-Detection:**
   - Detects whether running inside **Google Jules**, **OpenClaw**, **Google Antigravity**, **Claude Code**, or **Cursor**.
2. **Initial Setup Wizard Launch:**
   - Runs `python3 -m src.setup_wizard` to guide configuration.
3. **Hindsight Cloud API Key Prompt:**
   - Prompts for `HINDSIGHT_API_KEY` (securely masked, never logged, zero-leak).
4. **Instant Credential Validation:**
   - Pings Hindsight Cloud `/v1/default/banks` to verify authentication and low-latency connectivity.
5. **Memory Bank & Namespace Allocation:**
   - Configures dedicated memory banks for Deal Memory (`deals`) and Telemetry (`telemetry`).
6. **Pre-Flight Triad Health Check:**
   - Executes live tests for `RETAIN`, `RECALL`, and `REFLECT`. All three must pass before proceeding.
7. **Secondary MCP Configuration:**
   - Configures optional MCP servers (Neon PostgreSQL, Google Workspace, GitHub).
8. **Final Readiness Summary:**
   - Prints full operational status confirming the agent's cognitive brain is active.

---

## 3. Two-Dimensional Memory Model

DIAS organizes memory into two symbiotic dimensions stored in Vectorize Hindsight Cloud:

```
+--------------------------------------------------------------------------+
|                  VECTORIZE HINDSIGHT CLOUD MEMORY SYSTEM                 |
+--------------------------------------------------------------------------+
|  DIMENSION 1: DEAL DOMAIN MEMORY        |  DIMENSION 2: TELEMETRY MEMORY  |
|  Namespace: `dias_deals`                |  Namespace: `dias_telemetry`    |
|                                          |                                 |
|  • Stakeholder names & buying authority |  • User query intent patterns   |
|  • Technical prerequisites & compliance  |  • Repeated tool usage counts   |
|  • Competitor presence (Gong, Clari)    |  • Workflow friction & delays   |
|  • Budget caps & pricing objections      |  • Missing capability requests  |
|  • Procurement & legal terms            |  • Host agent performance stats |
+--------------------------------------------------------------------------+
                                     |
                                     v
                 [ REFLECTION & REASONING PIPELINE ]
                                     |
                                     v
               +-------------------------------------------+
               | Strategic Insights & Adaptive MCP Actions |
               +-------------------------------------------+
```

---

## 4. The Cognitive Triad Operations

### A. RETAIN (`memory_retain`)
Stores factual statements, meeting transcripts, and user events.
```json
{
  "namespace": "dias_deals",
  "key": "acme_corp_meeting_2",
  "data": {
    "deal_id": "DEAL-ACME-001",
    "customer": "Acme Corp",
    "event_type": "security_review",
    "content": "VP of Security confirmed AWS GovCloud and SOC2 compliance are mandatory. SSO via Okta required."
  }
}
```

### B. RECALL (`memory_recall`)
Semantic retrieval of past decisions and facts.
```json
{
  "namespace": "dias_deals",
  "query": "What security compliance does Acme Corp require?",
  "top_k": 5
}
```

### C. REFLECT (`memory_reflect`)
Synthesizes higher-order strategic beliefs and extracts operational patterns across interactions.
```json
{
  "namespace": "dias_deals",
  "topic": "deal_closing_risks"
}
```

---

## 5. Deal Intelligence & Narrative Generation

### Multi-Vector Health Scoring (`deal_analytics`)
Calculates an objective deal health score (1 to 100):
- **Engagement Momentum (25%):** Velocity and recency of buyer communication.
- **Stakeholder Depth (25%):** Multi-threaded executive buy-in (Champion, Economic Buyer, Security).
- **Technical Alignment (25%):** Resolution of architecture, SSO, and compliance blockers.
- **Commercial Feasibility (25%):** Budget clearance and contract timeline stability.

### Executive Deal Dossier (`generate_dossier`)
Compiles a polished ReportLab C-level PDF dossier containing:
- Executive Summary & Deal Vital Signs
- Health Radar & Risk Matrix
- Competitive Battlecard vs. Key Competitors
- Recommended Strategic Action Plan & Workspace Staging

### Workspace Follow-Up Staging (`stage_workspace`)
Safely drafts Gmail follow-ups and stages Calendar negotiation sessions with human-in-the-loop review.

---

## 6. Adaptive MCP Recommendation Engine

DIAS observes user activity and Hindsight reflection to propose dynamic MCP connections:

| Detected Interaction Pattern | Hindsight Reflection Insight | Recommended MCP Server | Benefit to User |
| :--- | :--- | :--- | :--- |
| **5+ database architecture queries** | Frequent relational schema lookups | **Neon PostgreSQL MCP** | Live schema queries & branch inspection |
| **Slack repeatedly mentioned** | Real-time deal alert needs | **Slack MCP** | Instant team deal notifications |
| **Salesforce CPQ discussed** | Complex enterprise pricing rules | **Salesforce Battlecards** | Dynamic competitive positioning |
| **Frequent scheduling friction** | Negotiation session delays | **Google Calendar MCP** | Automated executive calendar holds |

---

## 7. Day-by-Day Learning Progression

- **Day 1 / Interaction 1:** Generic baseline deal analysis.
- **Day 5 / Interaction 5:** Hindsight recalls AWS GovCloud and Okta SSO constraints; tailors technical narrative.
- **Day 20+ / Interaction 20+:** Full contextual mastery; recalls past pricing concessions, identifies buyer negotiation patterns, and proactively wires Neon PostgreSQL MCP for enterprise schema queries.
