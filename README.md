<div align="center">

# 🧠 Deal Intelligence Agent Skill (DIAS)
### *Autonomous Cognitive Sales Copilot for Hack with Hyderabad 2026*

```
PERSISTENT MEMORY  +  NEON DATABASE  +  GOOGLE WORKSPACE  +  DEAL INTELLIGENCE  =  DIAS
```

[![Hack with Hyderabad](https://img.shields.io/badge/Hack%20with%20Hyderabad-2026-FF5722?style=for-the-badge&logo=rocket&logoColor=white)](https://github.com/Manibhushanamk/HACKWITHHYD)
[![Tests](https://img.shields.io/badge/Tests-32%2F32%20Passed%20(100%25)-success?style=for-the-badge&logo=pytest&logoColor=white)](tests)
[![Cognitive Brain](https://img.shields.io/badge/Cognitive%20Brain-Vectorize%20Hindsight%20Cloud-4F46E5?style=for-the-badge&logo=cloud&logoColor=white)](https://vectorize.io)
[![Database](https://img.shields.io/badge/Relational%20DB-Neon%20Serverless%20Postgres-00E599?style=for-the-badge&logo=postgresql&logoColor=black)](https://neon.tech)
[![Workspace](https://img.shields.io/badge/Workspace-Google%20OAuth%202.0%20Desktop-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://workspace.google.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

<p align="center">
  <a href="#quick-start"><b>🚀 Quick Start</b></a> •
  <a href="#core-commands"><b>⌨️ Core Commands (/dias)</b></a> •
  <a href="#system-architecture"><b>🏗️ System Architecture</b></a> •
  <a href="#hindsight-is-the-cognitive-brain"><b>🧠 Hindsight Memory</b></a> •
  <a href="#neon-postgresql-persistence"><b>🐘 Neon PostgreSQL</b></a> •
  <a href="#google-workspace-integration"><b>📁 Google Workspace</b></a> •
  <a href="#verification"><b>🧪 Test Verification (32/32)</b></a>
</p>

</div>

---

> [!IMPORTANT]
> **Foundational Cognitive Substrate:** Traditional AI coding agents are stateless units that forget customer security mandates, pricing concessions, and compliance blockers between sessions. **DIAS** binds host coding agents (Google Jules, Antigravity, OpenClaw, Claude Code, Cursor) directly to **Vectorize Hindsight Cloud** for cognitive retention/recall, **Neon Serverless PostgreSQL** for structured persistence across 8 relational tables, and **Google Workspace** (Gmail, Calendar, Docs, Sheets, Drive) for automated, human-gated sales operations.

---

# 🚀 Quick Start

### 1. Clone & Set Up Virtual Environment

```bash
git clone https://github.com/Manibhushanamk/HACKWITHHYD.git
cd HACKWITHHYD

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment (`.env`)

Copy the template and provide your API keys:

```bash
cp .env.example .env
```

```env
# Vectorize Hindsight Cloud Configuration
HINDSIGHT_API_KEY="hsk_your_key_here"
HINDSIGHT_BASE_URL="https://api.hindsight.vectorize.io"

# Neon Serverless PostgreSQL
NEON_DATABASE_URL="postgresql://user:password@ep-your-pooler.c-6.us-east-2.aws.neon.tech/neondb?sslmode=require"

# Google Workspace Desktop OAuth
GOOGLE_CLIENT_SECRET_FILE="/path/to/client_secret_xxx.json"
GOOGLE_TOKEN_FILE="token.json"
```

### 3. Run the Full End-to-End Vertical Slice Demo

Executes a complete real-world scenario (Acme Corp $350k Deal in Security Review) across Neon DB, Hindsight Cloud, Google Workspace staging, and ReportLab PDF compilation:

```bash
python3 dias_cli.py --run-full-demo
```

### 4. Run the Full Automated Test Suite (32/32 Passed)

```bash
pytest tests/ -v
```

---

# ⌨️ Core Commands

DIAS provides two formal, agent-native slash commands registered for Google Antigravity, Claude Code, and Gemini:

### 1. `/dias` — Initialize Session & Gather Inputs

Start a new deal session or resume an active one.

```bash
# Check connectivity & launch input gathering
python3 dias_cli.py /dias

# Or pass natural language notes/transcripts directly
python3 dias_cli.py /dias --input "We have a $350k deal with Acme Corp in Security Review. Competitor is Gong. VP of Security requires AWS GovCloud and Okta SSO. Target close Nov 30, 2026."
```

**Lifecycle Steps:**
1. **Integration Audit**: Verifies Vectorize Hindsight Cloud, Neon PostgreSQL, and Google Workspace OAuth connectivity.
2. **First-Use OAuth Trigger**: Prompts Google OAuth consent flow via local webserver or out-of-band console if unauthenticated.
3. **Adaptive Extraction**: Normalizes deal metadata (deal ID, customer, value, stage, budget status, competitor, target close date).
4. **Epistemic Calibration**: Categorizes information into **Verified Facts**, **User Claims**, **Assumptions**, and **Unknowns**.
5. **Targeted Inquiries**: Prompts only for high-leverage missing fields rather than repeating already known data.

---

### 2. `/dias-input-end` — Conclude Input, Score & Generate Deliverables

Finalize data collection and trigger the autonomous analytical and delivery pipeline.

```bash
python3 dias_cli.py /dias-input-end
```

**Lifecycle Steps:**
1. **Epistemic Validation**: Asserts deal sanity (flags missing critical fields or unverified assumptions).
2. **Hindsight Semantic Recall**: Queries Hindsight memory banks (`dias_deals`, `dias_telemetry`) for historical customer disclosures and competitor battlecard intelligence.
3. **Transparent Deal Health Scoring**: Calculates an explainable 100-point Health Index and estimated win probability based on 4 weighted vectors.
4. **C-Level Executive Dossier Generation**: Compiles a publication-grade ReportLab PDF and Google Doc containing executive summaries, risk matrices, stakeholder maps, and competitive rebuttals.
5. **Google Sheets Master Deal Tracker Sync**: Automatically initializes or appends to the master deal pipeline spreadsheet with direct doc links and close dates.
6. **Workspace Human-in-the-Loop Actions**:
   - Creates a **Gmail follow-up draft** tailored to the deal stage (sending is strictly gated behind explicit confirmation).
   - Stages a **Google Calendar strategy hold** with duplicate-meeting collision detection.
7. **Dual-Layer Persistence**:
   - Relational records committed to **Neon PostgreSQL** across 8 tables.
   - Strategic takeaways inscribed into **Vectorize Hindsight Cloud** for perpetual future recall.

---

# 🏗️ Master System Architecture

```mermaid
flowchart TD
    User([Sales Engineer / Account Exec]) -->|"/dias"| Controller[DiasSessionController]
    User -->|Notes, Emails, Calls, SOWs| Controller

    subgraph Input & Epistemic Calibration
        Controller --> Profile[NormalizedDealProfile]
        Profile --> Epistemic[Epistemic Classifier<br/>• Verified Facts<br/>• User Claims<br/>• Assumptions<br/>• Unknowns]
    end

    User -->|"/dias-input-end"| Controller

    subgraph Cognitive Intelligence Layer
        Controller --> HindsightClient[Vectorize Hindsight Cloud]
        HindsightClient --> MemoryBanks[(Memory Banks:<br/>dias_deals<br/>dias_telemetry)]
        Controller --> Scorer[Transparent Deal Scorer<br/>100-Point Weighted Metric]
        Controller --> Battlecards[Competitive Battlecard Engine<br/>Gong / Clari / Salesforce]
    end

    subgraph Authoritative Relational Persistence
        Controller --> NeonDB[(Neon PostgreSQL<br/>8 Relational Tables)]
    end

    subgraph Deliverables & Workspace Staging
        Controller --> PDFGen[ReportLab PDF Engine<br/>12-Section Deal Dossier]
        Controller --> GDocs[Google Docs<br/>Executive Dossier]
        Controller --> GSheets[Google Sheets<br/>Master Deal Tracker]
        Controller --> GMail[Gmail Draft<br/>Human-in-the-Loop Gated]
        Controller --> GCal[Google Calendar<br/>Conflict-Checked Hold]
    end

    Controller --> Outputs[Actionable Executive Summary & Next Steps]
```

---

# 🧠 Hindsight Is the Cognitive Brain

Vectorize Hindsight Cloud is **the foundational cognitive brain** for DIAS. It partitions persistent knowledge into two distinct memory domains:

```
                              VECTORIZE HINDSIGHT CLOUD
                             (api.hindsight.vectorize.io)
                                           │
                     ┌─────────────────────┴─────────────────────┐
                     ▼                                           ▼
           DOMAIN 1: DEAL MEMORY                       DOMAIN 2: TELEMETRY
         Bank ID: 'dias_deals'                      Bank ID: 'dias_telemetry'
                     │                                           │
       • Buyer Objections & Needs                  • User Queries & Prompts
       • Technical Architecture (AWS GovCloud)     • Tool Invocations & Latency
       • Compliance Mandates (SOC2, Okta SAML)     • Workflow Friction Points
       • Commercial Terms & Seat Discounts         • Manual Repeated Lookups
```

### The Three-Phase Memory Cycle
1. **📥 RETAIN**: Inscribes deal facts and telemetry synchronously with retry backoff for embedding indexing (`POST /v1/default/banks/{bank_id}/memories`).
2. **🔍 RECALL**: Surfaces high-precision semantic memories prior to scoring (`POST /v1/default/banks/{bank_id}/memories/recall`), eliminating hallucination.
3. **💡 REFLECT**: Synthesizes higher-order strategic patterns and win/loss trends across past engagements (`POST /v1/default/banks/{bank_id}/reflect`).

---

# 🐘 Neon PostgreSQL Persistence

Structured deal records are authoritatively stored in **Neon Serverless PostgreSQL**.

### Optimized Connection Architecture
- Solves Linux IPv6 timeout hangs by resolving the primary IPv4 endpoint address dynamically and injecting `options='endpoint=ep-twilight-heart-b4629kfj-pooler'`.
- Sub-500ms connection latency across cloud sessions.

### Relational Schema (8 Tables)
1. **`deals`**: Authoritative deal master (ID, customer, contract value, stage, budget status, target close date, owner).
2. **`stakeholders`**: Champions, economic buyers, security gatekeepers, influence level, sentiment.
3. **`deal_interactions`**: Call transcripts, email logs, and touchpoint timelines.
4. **`deal_risks`**: Category, severity, probability, mitigation strategies.
5. **`deal_assessments`**: Health score, scoring component breakdown, model version, epistemic notes.
6. **`deal_actions`**: Recommended next steps, owners, deadlines, completion statuses.
7. **`dias_sessions`**: Session state, command history, serialized deal profile.
8. **`deal_documents`**: Google Doc IDs, Google Sheet links, local PDF file paths.

---

# 📁 Google Workspace Integration

DIAS integrates directly with Google Workspace using Desktop App OAuth 2.0 (`GoogleAuthManager`):

| Workspace Tool | Capability & Implementation Details | Human-in-the-Loop Safety |
|---|---|---|
| **Gmail** | Stages executive follow-up email drafts. | **Strictly Gated**: Real sends require explicit `user_confirmed=True`; otherwise blocked with `BLOCKED_REQUIRES_CONFIRMATION`. |
| **Google Calendar** | Schedules deal alignment meetings and strategy holds. | **Collision Detection**: Checks 2-hour surrounding window for conflicting events before staging. |
| **Google Docs** | Generates 12-section C-level executive Deal Dossiers. | Directly formatted with headings, tables, bullet points, and cloud access URL. |
| **Google Sheets** | Maintains the "DIAS Master Deal Tracker" spreadsheet. | Auto-creates sheet if missing and synchronizes deal row (Value, Stage, Close Date, Doc URL). |
| **Google Drive** | Indexes and links deal artifacts and attachments. | File search and parent folder reference tracking. |

---

# 🧪 Test Verification (32/32 Passing)

Every component is verified by an automated regression test suite:

```text
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0
rootdir: /home/kmanib/Documents/HACK WITH HYD/CODE
plugins: asyncio-1.4.0, anyio-4.15.1

tests/test_adaptive_mcp_setup.py ...                                     [  9%]
tests/test_dias_session_flow.py ..                                       [ 15%]
tests/test_dossier_compilation.py .                                      [ 18%]
tests/test_error_handling.py ........                                    [ 43%]
tests/test_google_workspace.py .....                                     [ 59%]
tests/test_hindsight_memory.py .....                                     [ 75%]
tests/test_neon_persistence.py .....                                     [ 90%]
tests/test_skill_invocation.py ...                                       [100%]

======================== 32 passed in 217.92s (0:03:37) ========================
```

| Test Suite | Tests | Assertions & Invariants Checked |
|---|---|---|
| `test_neon_persistence.py` | **5 / 5** | IPv4 connection, 8-table schema creation, deal upsert, stakeholder relations, document references. |
| `test_google_workspace.py` | **5 / 5** | Auth token refresh/fallback, Gmail draft creation, Human-in-the-loop send blocker, Calendar hold, Docs & Sheets sync. |
| `test_dias_session_flow.py` | **2 / 2** | `/dias` session initialization, `/dias-input-end` full deliverable pipeline, Neon & Hindsight sync. |
| `test_hindsight_memory.py` | **5 / 5** | API key masking, live ping, memory retain, semantic recall, reflection across banks. |
| `test_adaptive_mcp_setup.py` | **3 / 3** | Host agent sniffing (Jules, Antigravity, OpenClaw), setup wizard, telemetry pattern detection. |
| `test_error_handling.py` | **8 / 8** | Network failure, missing keys, 401 unauthorized, 404 routes, timeout retries. |
| `test_skill_invocation.py` | **3 / 3** | 4-vector scoring engine, workspace staging, JSON-RPC MCP dispatch. |
| `test_dossier_compilation.py` | **1 / 1** | ReportLab PDF compilation, styling, layout bounds, and file generation. |
| **TOTAL** | **32 / 32** | **100% Passing Regression Suite** |

---

# 💻 CLI Interface Reference

```bash
# Display service status and connection checks
python3 dias_cli.py /status

# Authenticate or refresh Google Workspace OAuth
python3 dias_cli.py /oauth

# Start a session
python3 dias_cli.py /dias --input "Deal with Acme Corp for $350k. VP of Security wants AWS GovCloud."

# Finalize and compile all assets
python3 dias_cli.py /dias-input-end

# One-command complete demo
python3 dias_cli.py --run-full-demo
```

---

<div align="center">
  <b>Built for Hack with Hyderabad 2026</b><br/>
  <i>Empowering enterprise sales teams with persistent cognitive intelligence and automated workflows.</i>
</div>
