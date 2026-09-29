# Deal Intelligence Agent Skill (DIAS) 🧠⚡

[![Tests](https://img.shields.io/badge/Tests-12%2F12%20Passed%20(100%25)-success?style=for-the-badge&logo=pytest)](file:///home/kmanib/deal-intelligence-skill/tests)
[![Cognitive Brain](https://img.shields.io/badge/Cognitive%20Brain-Vectorize%20Hindsight%20Cloud-blue?style=for-the-badge)](https://vectorize.io)
[![Protocol](https://img.shields.io/badge/MCP-Model%20Context%20Protocol%202.0-purple?style=for-the-badge)](https://modelcontextprotocol.io)
[![Database](https://img.shields.io/badge/Relational%20DB-Neon%20Serverless%20Postgres-00E599?style=for-the-badge&logo=postgresql)](https://neon.tech)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](file:///home/kmanib/deal-intelligence-skill/LICENSE)

> **Central Architectural Principle:**  
> **DIAS is a self-configuring, Hindsight-powered agent skill that establishes persistent memory during first-run installation, continuously retains and recalls deal and user context, reflects on accumulated interactions to learn patterns, and dynamically adapts its MCP capabilities as the user's workflow evolves.**  
> *Vectorize Hindsight Cloud is the Cognitive Brain and Central Memory Layer.*

---

## 🌟 HackwithHyderabad 3.0 Finale Submission Kit

* **Event:** HackwithHyderabad 3.0 Finale — Microsoft Hyderabad
* **Project Name:** Deal Intelligence Agent Skill (DIAS)
* **Skill Spec:** [SKILL.md](file:///home/kmanib/deal-intelligence-skill/SKILL.md) & [skill.yaml](file:///home/kmanib/deal-intelligence-skill/skill.yaml)
* **Master Plan PDF:** [DEAL_INTELLIGENCE_SKILL_MASTER_PLAN.pdf](file:///home/kmanib/Desktop/DEAL_INTELLIGENCE_SKILL_MASTER_PLAN.pdf)
* **Host Agent Compatibility:** Google Jules, OpenClaw, Google Antigravity, Claude Code, Cursor

---

## ⚡ 1-Click Universal Installation

Install and configure DIAS directly into your coding agent environment in one command:

```bash
# Clone and run universal Hindsight-first installer
git clone https://github.com/kmanib/deal-intelligence-skill.git
cd deal-intelligence-skill
./install.sh
```

Or run the interactive setup wizard directly:

```bash
python3 -m src.setup_wizard
```

---

## 🔄 8-Step Hindsight-First Installation Protocol

```
+-------------------------------------------------------------------------------+
|                 DIAS HINDSIGHT-FIRST INSTALLATION WORKFLOW                   |
+-------------------------------------------------------------------------------+
|  1. HOST AUTO-DETECTION  ──> Google Jules, OpenClaw, Antigravity, Claude Code  |
|  2. WIZARD LAUNCH        ──> Interactive CLI setup wizard initiates           |
|  3. HINDSIGHT API KEY    ──> First credential prompted (masked, zero-leak)    |
|  4. INSTANT VALIDATION   ──> Live ping to Vectorize Hindsight Cloud API       |
|  5. MEMORY BANK & NS     ──> Provisions 'dias_deals' & 'dias_telemetry'       |
|  6. PRE-FLIGHT TRIAD     ──> Automated tests for RETAIN, RECALL, REFLECT (PASS)|
|  7. SECONDARY MCPs       ──> Configures Neon PostgreSQL, Workspace, GitHub    |
|  8. FINAL SUMMARY        ──> System readiness confirmed; agent cognitive loop |
+-------------------------------------------------------------------------------+
```

---

## 🏗️ System Architecture

```
                       +---------------------------------------+
                       |   HOST CODING AGENT                   |
                       |   (Google Jules / OpenClaw / Claude)  |
                       +---------------------------------------+
                                          |
                                    MCP stdio / JSON-RPC
                                          v
                       +---------------------------------------+
                       |   DIAS CORE CONTROLLER                |
                       |   (src/core_skill.py)                 |
                       +---------------------------------------+
                                          |
         +--------------------------------+--------------------------------+
         |                                |                                |
         v                                v                                v
+------------------+            +-------------------+            +-------------------+
| HINDSIGHT CLIENT |            | DEAL SCORER &     |            | WORKSPACE STAGING |
| (Cognitive Brain)|            | DOSSIER GENERATOR |            | (Human-in-Loop)   |
| • Retain         |            | • Health (1-100)  |            | • Gmail Drafts    |
| • Recall         |            | • Win Prob %      |            | • Calendar Holds  |
| • Reflect        |            | • Executive PDF   |            | • Margin Guards   |
+------------------+            +-------------------+            +-------------------+
         |                                                                 |
         | (Domain 1 & 2)                                                  |
         v                                                                 v
+------------------+                                             +-------------------+
| HINDSIGHT CLOUD  |                                             | ADAPTIVE ROUTER   |
| • dias_deals     | ──[Reflection Insights & Telemetry Patterns]──> | Proactive MCP Recs|
| • dias_telemetry |                                             | (Neon, Slack, CPQ)|
+------------------+                                             +-------------------+
```

---

## 🧠 Two-Dimensional Memory Lifecycle

DIAS stores memory in two isolated, complementary dimensions within Vectorize Hindsight Cloud:

1. **Dimension 1: Deal Domain Memory (`dias_deals`)**
   - Stakeholder relationships & executive champions
   - Technical constraints (SOC2, AWS GovCloud, Okta SSO)
   - Competitor presence (Gong.io, Clari, Salesforce CPQ)
   - Commercial terms, discount history, and procurement milestones

2. **Dimension 2: Agent Telemetry & Usage Memory (`dias_telemetry`)**
   - User query intents and recurring questions
   - Tool invocation frequencies and friction points
   - Repeated database, messaging, or pricing requests
   - Adaptive trigger events for proactive MCP recommendations

---

## 🚀 The Cognitive Triad Operations

| Operation | MCP Tool | Purpose & Behavior |
| :--- | :--- | :--- |
| **RETAIN** | `memory_retain` | Inscribes sales transcripts, meeting facts, and telemetry into Hindsight Cloud memory banks. |
| **RECALL** | `memory_recall` | High-precision semantic retrieval of past decisions, buyer preferences, and technical prerequisites. |
| **REFLECT** | `memory_reflect` | Synthesizes higher-order strategic beliefs, identifies closing risks, and powers adaptive tool recommendations. |

---

## 📊 Multi-Vector Deal Health Scoring (1 to 100)

DIAS calculates holistic deal health across four 25-point weighted vectors:

```
+-------------------------------------------------------------------------------+
|                       MULTI-VECTOR DIAGNOSTIC RADAR                           |
+-------------------------------------------------------------------------------+
|  1. Engagement Momentum       [25%] ──> Velocity & recency of buyer contact   |
|  2. Stakeholder Coverage      [25%] ──> Multi-threaded Champion, Security, CFO|
|  3. Technical Alignment       [25%] ──> SOC2, Okta SAML, GovCloud resolution  |
|  4. Commercial Feasibility    [25%] ──> Budget clearance & margin guardrails  |
+-------------------------------------------------------------------------------+
```

---

## 🔌 Adaptive MCP Recommendation Engine

Unlike static agent skills, DIAS learns from user interaction friction and Hindsight memory reflections to proactively suggest and wire new MCP servers:

| Observed Workflow Friction | Hindsight Reflection Insight | Recommended MCP Server | Impact Score |
| :--- | :--- | :--- | :---: |
| **3+ Database/SQL queries** | Recurring queries against deal tables | **Neon PostgreSQL MCP** | **95** |
| **2+ Slack/messaging alerts** | Team collaboration & deal escalation | **Slack MCP** | **88** |
| **2+ Pricing/discount queries** | Complex enterprise discount thresholds | **Salesforce CPQ Battlecards** | **90** |
| **2+ Calendar friction events** | Executive availability bottlenecks | **Google Calendar MCP** | **85** |

---

## 📈 Day-by-Day Learning Progression

```
INTERACTION 1 (Day 1)          INTERACTION 5 (Day 5)         INTERACTION 20+ (Day 20+)
--------------------          ---------------------         -------------------------
• Generic baseline analysis    • Contextualized with memory   • Full contextual mastery
• Standard pipeline metrics    • Recalls AWS GovCloud & Okta  • Recalls multi-meeting history
• No historical memory         • Recommends battlecards       • Auto-wires Neon PostgreSQL MCP
• Basic deal score (60/100)    • Health score updated (78/100)• Compiles Executive PDF Dossier
```

---

## 🏢 Acme Corp Enterprise Deal Story

* **Day 1:** Acme Corp expresses interest in scaling sales intelligence across 150 enterprise reps. Initial deal analysis is generic.
* **Day 5:** VP of Security mandates AWS GovCloud hosting and Okta SSO. DIAS **retains** this disclosure into Hindsight Cloud. Upon next recall, DIAS automatically incorporates SOC2 Type II compliance into the technical narrative and raises deal health to 78/100.
* **Day 20+:** Procurement requests a 15% discount concession. DIAS **reflects** on historical margins, detects competitor bake-off with Gong.io, deploys the Gong battlecard, stages a tiered 100-seat licensing model, drafts the executive follow-up in Gmail, holds the Tuesday procurement review in Calendar, and generates the C-level Executive PDF Dossier.

---

## 🎬 3-Minute Demo Video Choreography

| Timecode | Visual Demonstration | Voiceover / Action Script |
| :--- | :--- | :--- |
| **0:00 - 0:45** | Terminal shows `./install.sh` running in Google Jules / OpenClaw. Masked Hindsight key input, live validation ping, and Pre-flight Triad check passing (100% PASS). | *"Welcome to DIAS—the Deal Intelligence Agent Skill. When downloaded from GitHub, DIAS establishes persistent memory first, validating Retain, Recall, and Reflect against Vectorize Hindsight Cloud."* |
| **0:45 - 1:30** | User introduces Acme Corp deal notes. Agent calls `memory_retain` and `memory_recall`. Screen highlights semantic extraction of AWS GovCloud and Okta SSO. | *"Unlike stateless tools, DIAS stores Acme Corp disclosures into Hindsight Cloud. When asked about security requirements, semantic recall instantly surfaces past compliance mandates."* |
| **1:30 - 2:15** | User asks 3 database queries about historical discount margins. Agent calls `memory_reflect`, detects database friction, and triggers Adaptive MCP recommendation for **Neon PostgreSQL**. | *"Notice how DIAS observes repeated SQL queries. Reflecting over telemetry, it dynamically recommends wiring the Neon PostgreSQL MCP server to inspect relational tables."* |
| **2:15 - 3:00** | Agent executes `generate_dossier` and opens `acme_corp_deal_dossier.pdf`. Displays multi-vector health scorecard (84/100), Gong battlecard, and staged Gmail follow-up. | *"Finally, DIAS compiles a C-level executive PDF deal dossier and stages Gmail drafts with human-in-the-loop review. This is the future of adaptive coding agent skills."* |

---

## ✅ Definition of Done (DoD) Verification

- [x] **One-Click Universal Installer:** `install.sh` with host agent detection (Google Jules, OpenClaw, Antigravity, Claude Code, Cursor).
- [x] **Hindsight-First Setup Wizard:** `src/setup_wizard.py` with masked input, live validation, and tenant namespace allocation.
- [x] **Pre-Flight Triad Health Check:** Automated live validation of `RETAIN`, `RECALL`, and `REFLECT` (all 3 passing).
- [x] **Two-Dimensional Memory Lifecycle:** Complete implementation of `dias_deals` and `dias_telemetry` namespaces in `src/memory/hindsight_client.py`.
- [x] **Multi-Vector Deal Health Scoring:** 1 to 100 scoring engine with momentum, stakeholders, technical, and commercial vectors (`src/analytics/deal_scorer.py`).
- [x] **Adaptive MCP Recommendation Engine:** Pattern detection and dynamic MCP wiring (`mcp/adaptive_router.py`).
- [x] **C-Level Executive PDF Dossier:** ReportLab compiler creating print-ready executive dossiers (`src/dossier/pdf_generator.py`).
- [x] **Human-in-the-Loop Workspace Staging:** Draft/holding safety controls for Gmail and Google Calendar (`src/workspace/workspace_mcp.py`).
- [x] **100% Test Pass Rate:** 12/12 unit and integration tests passing (`pytest tests/`).
- [x] **Zero Credential Leaking:** Masked terminal display and no committed secrets.

---

## 📂 Codebase Layout

```
deal-intelligence-skill/
├── SKILL.md                          <-- Universal Agent Skill Spec (Frontmatter + Prompts + Tool API)
├── skill.yaml                        <-- Manifest with auto-detection rules (Jules / OpenClaw / Antigravity)
├── README.md                         <-- GitHub documentation with live badges & 1-click install command
├── requirements.txt                  <-- Dependencies (mcp, pydantic, reportlab, psycopg2, requests)
├── install.sh                        <-- 1-click installer: auto-detects host agent & launches setup wizard
├── pyproject.toml                    <-- Package build configuration & entrypoints
├── mcp/
│   ├── __init__.py                   <-- MCP package export
│   ├── server.py                     <-- MCP server exposing all tools over standard JSON-RPC 2.0 stdio
│   ├── tools.json                    <-- Tool schemas (memory_retain, memory_recall, deal_score, dossier)
│   └── adaptive_router.py           <-- Dynamic MCP recommendations, pattern detection & auto-wiring
├── src/
│   ├── __init__.py                   <-- Core package export
│   ├── core_skill.py                 <-- Unified skill controller & entrypoint for coding agents
│   ├── setup_wizard.py               <-- Host detection, Hindsight API key validation & Pre-Flight Triad
│   ├── telemetry_analyzer.py         <-- Day-by-day telemetry logging, learning analysis & reflection
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── schema.py                 <-- Pydantic models for memories, telemetry, and extractions
│   │   └── hindsight_client.py       <-- Vectorize Hindsight Cloud SDK wrapper (retain, recall, reflect)
│   ├── analytics/
│   │   ├── __init__.py
│   │   └── deal_scorer.py            <-- Multi-vector health scoring (1-100) & win probability calculation
│   ├── narrative/
│   │   ├── __init__.py
│   │   └── battlecards.py            <-- Competitor battlecards (Gong, Clari, CPQ) & objection handling
│   ├── workspace/
│   │   ├── __init__.py
│   │   └── workspace_mcp.py          <-- Google Workspace staging (Gmail & Calendar) with human approval
│   └── dossier/
│       ├── __init__.py
│       └── pdf_generator.py          <-- ReportLab C-level executive PDF deal dossier compiler
└── tests/
    ├── __init__.py
    ├── test_hindsight_memory.py      <-- Tests Hindsight Cloud authentication, retain, recall, and reflect
    ├── test_adaptive_mcp_setup.py    <-- Validates setup wizard, key masking, and adaptive recommendation logic
    ├── test_skill_invocation.py      <-- Cross-agent skill execution verification
    └── test_dossier_compilation.py   <-- Validates ReportLab PDF generation and formatting
```
