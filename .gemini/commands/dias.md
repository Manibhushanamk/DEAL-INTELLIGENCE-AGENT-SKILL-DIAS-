---
description: Start or resume a Deal Intelligence Agent Skill (DIAS) session, verify integrations, check Google OAuth, and collect deal details.
---

# /dias Command

When the user invokes `/dias`:

1. Initialize or resume the DIAS session controller using `src.session.controller.DiasSessionController`.
2. Audit active connectivity to:
   - **Vectorize Hindsight Cloud** (Persistent Cognitive Brain)
   - **Neon PostgreSQL** (Authoritative Structured Deal Database)
   - **Google Workspace** (Gmail, Calendar, Docs, Sheets Desktop OAuth)
3. If Google OAuth is not yet connected, offer to launch the local OAuth consent server.
4. Report integration statuses clearly to the user.
5. Ingest any user-provided notes, customer names, contract values, requirements, or deal IDs.
6. Display the current normalized deal profile (customer, value, stage, budget, competition, requirements, timeline).
7. Ask targeted discovery questions if essential information is missing.
8. Persist the session snapshot into Neon PostgreSQL.
