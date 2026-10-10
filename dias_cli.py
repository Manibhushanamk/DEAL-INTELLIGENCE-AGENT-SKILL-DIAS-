#!/usr/bin/env python3
"""
DIAS Command-Line Interface (CLI).
Provides interactive and automated execution of the two core DIAS commands:
  - `/dias`: Start or resume session, audit integrations & OAuth, ingest deal data.
  - `/dias-input-end`: Validate inputs, run multi-vector analysis, generate PDF & Google Workspace deliverables, persist to Neon & Hindsight.
"""

import sys
import os
import json
import argparse
from typing import Optional

# Ensure repository root is on Python sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from src.core_skill import DealIntelligenceSkill
from src.session.controller import DiasSessionController


def print_banner():
    print("""
========================================================================
  DIAS — DEAL INTELLIGENCE AGENT SKILL
  Cognitive Brain: Vectorize Hindsight Cloud
  Structured DB:   Neon PostgreSQL
  Workspace:       Google Workspace (Gmail, Calendar, Docs, Sheets)
========================================================================
Commands supported:
  /dias           - Start/resume session, audit integrations, input deal info
  /dias-input-end - Validate inputs, score deal, generate dossier, persist data
  /oauth          - Trigger interactive Google OAuth authorization
  /status         - Display active deal profile and integration connectivity
  /exit           - Exit session
========================================================================
""")


def format_integrations_report(integrations: dict) -> str:
    lines = []
    lines.append("\n[INTEGRATION HEALTH STATUS]")
    hs = integrations.get("hindsight_cloud", {})
    lines.append(f"  • Hindsight Cloud:   {hs.get('status')} ({hs.get('message', '')})")
    neon = integrations.get("neon_postgresql", {})
    lines.append(f"  • Neon PostgreSQL:   {neon.get('status')} ({neon.get('message', '')})")
    gw = integrations.get("google_workspace", {})
    user = f" [{gw.get('user_email')}]" if gw.get('user_email') else ""
    lines.append(f"  • Google Workspace:  {gw.get('status')}{user} (Desktop Client: {'Configured' if gw.get('client_secret_configured') else 'Missing'})")
    return "\n".join(lines)


def format_deal_profile(profile: dict) -> str:
    lines = []
    lines.append("\n[CURRENT DEAL PROFILE]")
    lines.append(f"  • Deal ID:        {profile.get('deal_id')}")
    lines.append(f"  • Customer:       {profile.get('customer')}")
    lines.append(f"  • Value:          ${profile.get('value', 0):,.2f} {profile.get('currency', 'USD')}")
    lines.append(f"  • Stage:          {profile.get('stage')}")
    lines.append(f"  • Budget Status:  {profile.get('budget_status')}")
    lines.append(f"  • Competition:    {profile.get('competition')}")
    reqs = profile.get('requirements', [])
    lines.append(f"  • Requirements:   {', '.join(reqs) if reqs else 'None specified'}")
    lines.append(f"  • Target Close:   {profile.get('timeline')}")
    return "\n".join(lines)


def run_interactive_loop(controller: DiasSessionController):
    print_banner()
    print("Welcome to DIAS. Type `/dias` to initialize a session or enter deal details.\n")

    while True:
        try:
            user_line = input("DIAS > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting DIAS session. Goodbye.")
            break

        if not user_line:
            continue

        if user_line in ["/exit", "exit", "quit"]:
            print("Session ended.")
            break

        elif user_line.startswith("/dias-input-end"):
            print("\n[DIAS] Ending input collection. Initiating analysis & deliverable pipeline...")
            res = controller.handle_dias_input_end_command()
            print("\n" + "=" * 70)
            print(f"  DIAS ANALYSIS COMPLETE — {res.get('customer')}")
            print("=" * 70)
            print(f"  • Health Score:    {res.get('health_score')}")
            print(f"  • Win Probability: {res.get('win_probability')}")
            print("\n[DELIVERABLES GENERATED]")
            deliv = res.get("deliverables", {})
            print(f"  📄 Executive PDF:   {deliv.get('pdf_dossier')}")
            print(f"  📝 Google Doc:      {deliv.get('google_doc')}")
            print(f"  📊 Master Sheet:    {deliv.get('master_google_sheet')}")
            print(f"  ✉️  Gmail Draft:     {deliv.get('gmail_draft')}")
            print(f"  📅 Calendar Hold:   {deliv.get('calendar_hold')}")
            print("\n[PERSISTENCE VERIFICATION]")
            persist = res.get("persistence", {})
            print(f"  🗄️  Neon DB:         {persist.get('neon_postgresql')}")
            print(f"  🧠 Hindsight Cloud: {persist.get('hindsight_cloud')}")
            print("=" * 70 + "\n")

        elif user_line.startswith("/dias"):
            # Extract any inline text after /dias
            parts = user_line.split(" ", 1)
            extra_text = parts[1] if len(parts) > 1 else None
            res = controller.handle_dias_command(user_input=extra_text)
            print(format_integrations_report(res["integrations"]))
            print(format_deal_profile(res["deal_profile"]))
            validation = res["validation"]
            if validation["missing_essential_fields"]:
                print("\n[TARGETED DISCOVERY QUESTIONS]")
                for q in validation["targeted_clarification_questions"]:
                    print(f"  ❓ {q}")
            print(f"\n👉 {res['next_step']}\n")

        elif user_line == "/oauth":
            print("\n[DIAS] Launching Google OAuth desktop consent flow...")
            ok, msg = controller.google.auth.initiate_authorization_flow()
            print(f"OAuth Result: {'✓ SUCCESS' if ok else '✗ FAILED'} ({msg})\n")

        elif user_line == "/status":
            print(format_deal_profile(controller.profile.to_dict()))
            ok, msg, counts = controller.neon.health_check()
            print(f"\nNeon PostgreSQL: {'CONNECTED' if ok else 'OFFLINE'} | Records: {counts}")
            print(f"Hindsight Cloud: {'CONNECTED' if controller.hindsight.validate_connection()[0] else 'OFFLINE'}")
            print(f"Google Workspace: {'AUTHORIZED' if controller.google.is_connected() else 'PENDING_OAUTH'}\n")

        else:
            # Treat generic input as ongoing deal notes
            controller.profile.ingest_text(user_line)
            controller._persist_session_state()
            print(f"✓ Ingested deal notes. Customer: '{controller.profile.customer}' | Value: ${controller.profile.value:,.2f}")
            print("Type `/dias-input-end` when finished to generate analysis & dossier.")


def main():
    parser = argparse.ArgumentParser(description="DIAS - Deal Intelligence Agent Skill CLI")
    parser.add_argument("command", nargs="?", default=None, help="Command to run (/dias, /dias-input-end, or demo)")
    parser.add_argument("--input", type=str, default=None, help="Deal input notes or transcript")
    parser.add_argument("--deal-id", type=str, default=None, help="Deal ID to load or analyze")
    parser.add_argument("--file", type=str, default=None, help="File to ingest")
    parser.add_argument("--oauth", action="store_true", help="Trigger Google OAuth desktop flow")
    parser.add_argument("--run-full-demo", action="store_true", help="Execute complete automated end-to-end demo")
    args = parser.parse_args()

    controller = DiasSessionController()

    if args.run_full_demo:
        print_banner()
        print("[DIAS DEMO] Executing complete automated end-to-end deal intelligence flow...")
        print("\nStep 1: Running /dias with Acme Corp enterprise notes...")
        demo_text = (
            "We have a $350,000 enterprise deal with Acme Corp currently in Security Review stage. "
            "VP of Engineering (Sarah Chen) and CISO mandate Okta SSO and AWS GovCloud compliance. "
            "Primary competitor is Gong. Target close is End of Q4 2026. Budget is formally approved."
        )
        dias_res = controller.handle_dias_command(user_input=demo_text)
        print(format_integrations_report(dias_res["integrations"]))
        print(format_deal_profile(dias_res["deal_profile"]))

        print("\nStep 2: Running /dias-input-end for full analysis & deliverable compilation...")
        end_res = controller.handle_dias_input_end_command()
        print("\n" + "=" * 70)
        print(f"  DIAS ANALYSIS COMPLETE — {end_res.get('customer')}")
        print("=" * 70)
        print(f"  • Health Score:    {end_res.get('health_score')}")
        print(f"  • Win Probability: {end_res.get('win_probability')}")
        print("\n[DELIVERABLES GENERATED]")
        deliv = end_res.get("deliverables", {})
        print(f"  📄 Executive PDF:   {deliv.get('pdf_dossier')}")
        print(f"  📝 Google Doc:      {deliv.get('google_doc')}")
        print(f"  📊 Master Sheet:    {deliv.get('master_google_sheet')}")
        print(f"  ✉️  Gmail Draft:     {deliv.get('gmail_draft')}")
        print(f"  📅 Calendar Hold:   {deliv.get('calendar_hold')}")
        print("\n[PERSISTENCE VERIFICATION]")
        persist = end_res.get("persistence", {})
        print(f"  🗄️  Neon DB:         {persist.get('neon_postgresql')}")
        print(f"  🧠 Hindsight Cloud: {persist.get('hindsight_cloud')}")
        print("=" * 70 + "\n")
        return

    if args.command == "/dias":
        res = controller.handle_dias_command(user_input=args.input, deal_id=args.deal_id, file_path=args.file, interactive_oauth=args.oauth)
        print(format_integrations_report(res["integrations"]))
        print(format_deal_profile(res["deal_profile"]))
        print(f"\n{res['next_step']}")
        return

    if args.command == "/dias-input-end":
        res = controller.handle_dias_input_end_command()
        print(json.dumps(res, indent=2))
        return

    # Interactive mode
    run_interactive_loop(controller)


if __name__ == "__main__":
    main()
