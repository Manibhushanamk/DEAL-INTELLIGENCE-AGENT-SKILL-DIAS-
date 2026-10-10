---
description: Conclude deal input collection, perform multi-vector analysis, generate PDF & Google Workspace deliverables, and persist records to Neon & Hindsight.
---

# /dias-input-end Command

When the user invokes `/dias-input-end`:

1. Validate the collected deal profile.
2. Recall relevant historical deal context and objections from **Vectorize Hindsight Cloud** (`dias_deals`).
3. Run multi-vector health scoring (Momentum, Stakeholder Multi-Threading, Technical Alignment, Commercial Feasibility) to compute overall score (1-100) and win probability %.
4. Retrieve competitive battlecards (e.g. Gong, Clari) and identify key objection counters.
5. Generate an executive **ReportLab PDF Deal Dossier** in `reports/`.
6. Generate a 12-section **Google Doc Deal Report** via Google Docs API.
7. Create or update the **Master Deal Tracker Google Sheet** with deal metrics, timeline, and doc link.
8. Stage a personalized **Gmail follow-up draft** (human-in-the-loop review) and **Google Calendar alignment hold**.
9. Persist structured deal, stakeholder, assessment, risk, and action records into **Neon PostgreSQL**.
10. Inscribe permanent deal facts and telemetry into **Vectorize Hindsight Cloud** (`dias_deals` and `dias_telemetry`).
11. Output a comprehensive executive summary to the user with all generated links and next steps.
