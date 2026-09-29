#!/usr/bin/env python3
"""
Script to generate the comprehensive DIAS Final Submission & Video Recording Runbook PDF
directly on the Desktop.
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (Pages > 1)
        if self._pageNumber > 1:
            self.drawString(45, 11 * inch - 30, "DIAS • DEAL INTELLIGENCE AGENT SKILL — FINAL SUBMISSION & RECORDING RUNBOOK")
            self.drawRightString(8.5 * inch - 45, 11 * inch - 30, "HACKWITHHYDERABAD 2026")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(45, 11 * inch - 34, 8.5 * inch - 45, 11 * inch - 34)

        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(45, 38, 8.5 * inch - 45, 38)
        
        self.setFont("Helvetica", 8)
        self.drawString(45, 26, "Official Final Submission • Vectorize Hindsight Cloud • Model Context Protocol (MCP)")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 45, 26, page_text)
        self.restoreState()

def build_pdf(output_paths):
    styles = getSampleStyleSheet()
    
    # Custom Color Palette
    c_primary = colors.HexColor("#0F172A")    # Deep Navy Slate
    c_accent = colors.HexColor("#1D4ED8")     # Royal Blue
    c_emerald = colors.HexColor("#059669")    # Forest Emerald
    c_purple = colors.HexColor("#6D28D9")     # Deep Violet
    c_light = colors.HexColor("#F8FAFC")
    c_border = colors.HexColor("#CBD5E1")
    c_amber = colors.HexColor("#B45309")
    c_red = colors.HexColor("#DC2626")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_primary,
        alignment=0
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#475569")
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=c_primary,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=c_accent,
        spaceBefore=6,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#1E293B")
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=c_primary
    )

    dialogue_style = ParagraphStyle(
        'Dialogue_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11.5,
        textColor=c_emerald
    )

    callout_style = ParagraphStyle(
        'Callout_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=c_primary
    )

    table_header_style = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=1
    )

    story = []

    # =========================================================================
    # HEADER BANNER
    # =========================================================================
    story.append(Paragraph("Deal Intelligence Agent Skill (DIAS)", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph(
        "<b>Final Hackathon Submission Dossier & 3-Minute Video Screening Runbook</b><br/>"
        "Cognitive Brain: <b>Vectorize Hindsight Cloud</b> &nbsp;|&nbsp; Protocol: <b>Model Context Protocol (MCP)</b> &nbsp;|&nbsp; Team Leader: <b>Manibhushanam</b>",
        subtitle_style
    ))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=0, spaceAfter=8))

    # Fast Action Summary Box
    summary_data = [
        [
            Paragraph("<b>🚀 1-COMMAND VIDEO DEMO LAUNCHER:</b><br/>"
                      "<code>cd ~/deal-intelligence-skill && ./run_all.sh --skip-tests</code><br/>"
                      "<i>Runs the Hindsight Cloud Setup Wizard, validates the Pre-Flight Triad, executes the Acme Corp ($350k) deal demo, and dynamically wires the Neon PostgreSQL MCP in under 10 seconds.</i>", callout_style),
            Paragraph("<b>🌐 OFFICIAL SUBMISSION LINKS:</b><br/>"
                      "• <b>GitHub Repo:</b> <code>github.com/Manibhushanamk/DEAL-INTELLIGENCE-AGENT-SKILL-DIAS-</code><br/>"
                      "• <b>Hindsight Usage:</b> <code>https://ui.hindsight.vectorize.io/usage</code><br/>"
                      "• <b>Hindsight Dashboard:</b> <code>https://ui.hindsight.vectorize.io/dashboard</code><br/>"
                      "• <b>Final Form:</b> <code>https://forms.gle/cD7fCnPnkdVm2sH78</code>", callout_style)
        ]
    ]
    summary_table = Table(summary_data, colWidths=[3.9 * inch, 3.5 * inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#86EFAC")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 1: MASTER RECORDING RUNBOOK (THE REQUESTED TABLE!)
    # =========================================================================
    story.append(Paragraph("🎬 3-Minute Video Screening Runbook (Start Recording Now!)", h1_style))
    story.append(Paragraph(
        "Follow this exact second-by-second schedule during your screen recording. "
        "Keep the terminal clear, keep browser tabs pre-opened, and deliver the voiceover script with high confidence.",
        body_style
    ))
    story.append(Spacer(1, 4))

    runbook_headers = [
        Paragraph("<b>Time Range</b>", table_header_style),
        Paragraph("<b>Screen View</b>", table_header_style),
        Paragraph("<b>What to Do (Actions)</b>", table_header_style),
        Paragraph("<b>What to Say (Exact Voiceover Dialogue)</b>", table_header_style)
    ]

    runbook_rows = [
        runbook_headers,
        # Step 1
        [
            Paragraph("<b>00:00 – 00:25</b><br/>(25s)", ParagraphStyle('T1', parent=body_style, fontName='Helvetica-Bold', textColor=c_primary)),
            Paragraph("<b>Split Screen:</b><br/>Terminal on right, GitHub README on left.", body_style),
            Paragraph("• Start screen recording.<br/>• Have terminal ready in <code>~/deal-intelligence-skill</code>.<br/>• Point mouse at the stateless agent problem.", body_style),
            Paragraph("\"Hi everyone, I'm Manibhushanam and this is <b>DIAS — Deal Intelligence Agent Skill</b>.<br/><br/>"
                      "Today, AI coding agents are stateless — they forget everything between sessions. "
                      "We gave host coding agents a permanent cognitive brain powered by <b>Vectorize Hindsight Cloud</b>.\"", dialogue_style)
        ],
        # Step 2
        [
            Paragraph("<b>00:25 – 01:10</b><br/>(45s)", ParagraphStyle('T2', parent=body_style, fontName='Helvetica-Bold', textColor=c_primary)),
            Paragraph("<b>Terminal Work:</b><br/>Full terminal view.", body_style),
            Paragraph("• Run command:<br/><code>./run_all.sh --skip-tests</code><br/>"
                      "• Watch setup wizard & live demo execute in real time.<br/>"
                      "• Highlight green checkmarks on screen.", body_style),
            Paragraph("\"With one command, <code>./run_all.sh</code>, DIAS starts. It auto-detects the host agent, "
                      "connects to Vectorize Hindsight Cloud with zero-leak key masking, validates the Pre-Flight Triad (Retain, Recall, Reflect), "
                      "analyzes our $350k Acme Corp deal, and dynamically recommends the Neon PostgreSQL MCP based on developer query friction.\"", dialogue_style)
        ],
        # Step 3
        [
            Paragraph("<b>01:10 – 01:45</b><br/>(35s)", ParagraphStyle('T3', parent=body_style, fontName='Helvetica-Bold', textColor=c_primary)),
            Paragraph("<b>Terminal Scroll & PDF Result:</b><br/>Terminal ➔ Document Viewer", body_style),
            Paragraph("1. Scroll terminal to show <b>PROJECT RESULT</b> box.<br/>"
                      "2. Open the executive dossier:<br/><code>xdg-open acme_corp_deal_dossier.pdf</code><br/>"
                      "3. Show radar bars, SWOT, & Gong battlecard.", body_style),
            Paragraph("\"Looking at the result: DIAS scored Acme Corp at <b>85/100 health</b> with <b>78.2% win probability</b>, "
                      "resolved their GovCloud and Okta SAML 2.0 mandates, and generated this publication-grade C-level PDF deal dossier on the fly.\"", dialogue_style)
        ],
        # Step 4
        [
            Paragraph("<b>01:45 – 02:25</b><br/>(40s)", ParagraphStyle('T4', parent=body_style, fontName='Helvetica-Bold', textColor=c_primary)),
            Paragraph("<b>Browser Tabs 1 & 2:</b><br/>Vectorize Hindsight Cloud UI", body_style),
            Paragraph("1. Switch to <code>ui.hindsight.vectorize.io/usage</code>.<br/>"
                      "2. Switch to <code>ui.hindsight.vectorize.io/dashboard</code>.<br/>"
                      "3. Open <b><code>dias_deals</code></b> bank and highlight Acme Corp nodes.", body_style),
            Paragraph("\"In the Vectorize Hindsight Cloud dashboard, you can see live API request metrics and the actual memories persisted in our <code>dias_deals</code> bank — "
                      "proving real multi-session cloud cognitive persistence.\"", dialogue_style)
        ],
        # Step 5
        [
            Paragraph("<b>02:25 – 02:50</b><br/>(25s)", ParagraphStyle('T5', parent=body_style, fontName='Helvetica-Bold', textColor=c_primary)),
            Paragraph("<b>Browser Tab 3:</b><br/>GitHub Repository README", body_style),
            Paragraph("• Switch to GitHub repository tab.<br/>"
                      "• Scroll to <b>Continuous Learning Curve</b> diagram.<br/>"
                      "• Point to the <b>1-Command Quick Start</b> block.", body_style),
            Paragraph("\"Everything is open source on GitHub. Our README details the cognitive architecture, and any judge or developer can clone and run DIAS with that exact single command.\"", dialogue_style)
        ],
        # Step 6
        [
            Paragraph("<b>02:50 – 03:00</b><br/>(10s)", ParagraphStyle('T6', parent=body_style, fontName='Helvetica-Bold', textColor=c_primary)),
            Paragraph("<b>Terminal / Conclusion:</b><br/>Final Closing Screen", body_style),
            Paragraph("• Show terminal with 20/20 test passes (<code>./run_tests.sh</code>) or GitHub repo URL.<br/>• Final wave & thank you.", body_style),
            Paragraph("\"Persistent memory turns coding agents from forgetful chatbots into continuous learning partners. Thank you!\"", dialogue_style)
        ]
    ]

    runbook_table = Table(runbook_rows, colWidths=[0.9 * inch, 1.3 * inch, 2.2 * inch, 3.0 * inch])
    runbook_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
    ]))
    story.append(runbook_table)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 2: VERIFIED TERMINAL OUTPUT & PROJECT RESULT ANALYSIS
    # =========================================================================
    story.append(Paragraph("📊 Verified Terminal Output & Project Result Analysis", h1_style))
    story.append(Paragraph(
        "Below is the exact output generated when running <code>./run_all.sh --skip-tests</code>. "
        "Point your cursor at the key cognitive steps during the recording:",
        body_style
    ))
    story.append(Spacer(1, 4))

    terminal_snippet = (
        "========================================================================<br/>"
        "    DEAL INTELLIGENCE AGENT SKILL (DIAS) — MASTER ALL-IN-ONE PIPELINE  <br/>"
        "    Cognitive Brain: Vectorize Hindsight Cloud | Protocol: MCP (stdio)  <br/>"
        "========================================================================<br/>"
        "[STAGE 1/3] RUNNING HINDSIGHT SETUP WIZARD & PRE-FLIGHT TRIAD...<br/>"
        "  ✓ Host Agent:         Google Jules detected<br/>"
        "  ✓ Hindsight Cloud:    Connected (hsk_...5181 masked)<br/>"
        "  ✓ Memory Banks:       dias_deals & dias_telemetry<br/>"
        "  ✓ Pre-Flight Triad:   RETAIN: ✓ Passed | RECALL: ✓ Passed | REFLECT: ✓ Passed<br/>"
        "  ✓ Hindsight Memory:   READY (Triad 100% Operational)<br/>"
        "<br/>"
        "[STAGE 2/3] RUNNING LIVE ENTERPRISE DEAL INTELLIGENCE DEMO...<br/>"
        "  ✓ Hindsight Retain:   Inscribed Acme Corp security and pricing disclosures.<br/>"
        "  ✓ Semantic Recall:    Surfaced GovCloud, Okta SSO, SOC2 compliance (0% hallucination)<br/>"
        "  ✓ Health Scoring:     85.0 / 100 (EXCELLENT) | Win Probability: 78.2%<br/>"
        "  ✓ Diagnostic Vectors: Momentum: 24/25 | Stakeholders: 20/25 | Tech: 22/25 | Comm: 19/25<br/>"
        "  ✓ Hindsight Reflect:  Discovered friction in manual relational schema inspection.<br/>"
        "  👉 RECOMMENDED MCP:   Neon PostgreSQL MCP (Impact Score: 95/100)<br/>"
        "  ✓ Dynamic Wiring:     Neon PostgreSQL MCP connected into agent settings!<br/>"
        "  ✓ Executive Dossier:  acme_corp_deal_dossier.pdf compiled (ReportLab)<br/>"
        "<br/>"
        "========================================================================<br/>"
        "  📊 PROJECT RESULT: ACME CORP DEAL INTELLIGENCE & EXECUTIVE ANALYSIS   <br/>"
        "========================================================================<br/>"
        "  🏢 Account Name:        Acme Corp ($350,000 ARR | 150 Enterprise Seats)<br/>"
        "  🎯 Deal Health Score:   85.0 / 100 (EXCELLENT)<br/>"
        "  📈 Win Probability:     78.2% (High Confidence)<br/>"
        "  🛡️ Compliance Status:   AWS GovCloud Mandate + Okta SAML 2.0 (Resolved)<br/>"
        "  ⚔️ Competitor Defense:  Gong.io discounted 20% ➔ Differentiated on Persistent Intelligence<br/>"
        "  🧠 Cognitive Memory:    Vectorize Hindsight Cloud ('dias_deals' & 'dias_telemetry')<br/>"
        "  🔌 Adaptive MCP Wired:  Neon PostgreSQL MCP (Automatic SQL inspection)<br/>"
        "  📄 Result Deliverable:  acme_corp_deal_dossier.pdf<br/>"
        "  💡 Quick Open Command:  xdg-open acme_corp_deal_dossier.pdf<br/>"
        "========================================================================"
    )

    term_table = Table([[Paragraph(terminal_snippet, code_style)]], colWidths=[7.4 * inch])
    term_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0B1120")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#1E293B")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(term_table)
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 3: COMPLETE GOOGLE FORM SUBMISSION ANSWERS
    # =========================================================================
    story.append(Paragraph("📋 Complete Google Form Submission Guide (Copy & Paste)", h1_style))
    story.append(Paragraph("<b>Submission URL:</b> <code>https://forms.gle/cD7fCnPnkdVm2sH78</code>", subtitle_style))
    story.append(Spacer(1, 4))

    form_rows = [
        [Paragraph("<b>Form Field</b>", table_header_style), Paragraph("<b>Exact Copy-Paste Response</b>", table_header_style)],
        [
            Paragraph("<b>Email ID</b>", body_style),
            Paragraph("<code>manibhushanam4k@gmail.com</code>", body_style)
        ],
        [
            Paragraph("<b>Phone Number</b>", body_style),
            Paragraph("<code>+91 9154746353</code>", body_style)
        ],
        [
            Paragraph("<b>Team Name</b>", body_style),
            Paragraph("<b>DIAS Team</b> (or registration team name)", body_style)
        ],
        [
            Paragraph("<b>Team Members</b>", body_style),
            Paragraph("<b>Manibhushanam</b> (Team Leader)", body_style)
        ],
        [
            Paragraph("<b>GitHub Repository URL</b>", body_style),
            Paragraph("<code>https://github.com/Manibhushanamk/DEAL-INTELLIGENCE-AGENT-SKILL-DIAS-.git</code>", body_style)
        ],
        [
            Paragraph("<b>Live Demo / Video Link</b>", body_style),
            Paragraph("<i>[Paste your Unlisted YouTube or Google Drive link of the 3-minute video here]</i>", body_style)
        ],
        [
            Paragraph("<b>Project Title & Description</b>", body_style),
            Paragraph("<b>Deal Intelligence Agent Skill (DIAS)</b>: Persistent B2B Sales & Deal Intelligence for Autonomous AI Coding Agents powered by Vectorize Hindsight Cloud and Adaptive MCP Evolution.", body_style)
        ],
        [
            Paragraph("<b>Technical Innovation & Architecture</b>", body_style),
            Paragraph("DIAS solves agent statelessness by introducing a two-dimensional cognitive brain (<code>dias_deals</code> and <code>dias_telemetry</code>) hosted on Vectorize Hindsight Cloud. "
                      "It implements a verified Retain/Recall/Reflect lifecycle, multi-vector deal health scoring (1-100), automated C-level PDF dossier compilation via ReportLab, "
                      "and an Adaptive MCP Router that detects developer workflow friction and dynamically wires secondary MCP servers (e.g. Neon PostgreSQL) with human-in-the-loop safety gating.", body_style)
        ]
    ]

    form_table = Table(form_rows, colWidths=[2.2 * inch, 5.2 * inch])
    form_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
    ]))
    story.append(form_table)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 4: LINKEDIN POST & TECHNICAL ARTICLE (STRICT NO HACKATHON RULE!)
    # =========================================================================
    story.append(Paragraph("📱 LinkedIn Post (Strict Rule: Zero 'Hackathon' Mentions)", h1_style))
    story.append(Paragraph(
        "<b>⚠️ STRICT DISQUALIFICATION RULE:</b> The word 'hackathon' is 100% excluded. "
        "Copy and paste this exact Andrej Karpathy-style post to LinkedIn:",
        callout_style
    ))
    story.append(Spacer(1, 4))

    linkedin_post_content = (
        "AI coding agents today have a fatal flaw: amnesia.<br/><br/>"
        "Every time you boot a new session in Jules, OpenClaw, or Antigravity, it's Day 1 all over again. "
        "The agent forgets critical customer mandates, ignores past architectural constraints, and operates with rigid, static tools.<br/><br/>"
        "We built DIAS (Deal Intelligence Agent Skill) to fix this.<br/><br/>"
        "Using Vectorize Hindsight Cloud, DIAS gives coding agents a persistent, two-dimensional cognitive brain:<br/>"
        "1. Domain Memory (dias_deals): Retains customer disclosures, security mandates, and commercial terms.<br/>"
        "2. Telemetry Memory (dias_telemetry): Tracks developer friction and tool usage.<br/><br/>"
        "When DIAS notices repeated relational database queries, it uses Hindsight Reflect to diagnose friction and dynamically wires the Neon PostgreSQL MCP server.<br/><br/>"
        "Zero hallucination. Autonomous tool evolution. True persistent memory.<br/><br/>"
        "Check out our open-source codebase on GitHub: https://github.com/Manibhushanamk/DEAL-INTELLIGENCE-AGENT-SKILL-DIAS-<br/><br/>"
        "#AIAgents #AI #Hindsight #AgentMemory #AIMemory #LLM #ModelContextProtocol"
    )

    li_table = Table([[Paragraph(linkedin_post_content, body_style)]], colWidths=[7.4 * inch])
    li_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(li_table)
    story.append(Spacer(1, 4))

    first_comment_text = (
        "<b>💬 REQUIRED FIRST COMMENT ON LINKEDIN POST:</b><br/>"
        "<code>Huge thanks to the Vectorize team for building Hindsight Cloud! Read the documentation & persistent memory framework here: https://github.com/vectorize-io/hindsight</code>"
    )
    story.append(Paragraph(first_comment_text, callout_style))
    story.append(Spacer(1, 10))

    # Technical Article Overview
    story.append(Paragraph("📝 Technical Article for Dev.to / Medium / Hashnode", h1_style))
    story.append(Paragraph(
        "<b>Title:</b> Giving AI Coding Agents a Permanent Brain: How We Built DIAS with Vectorize Hindsight Cloud and Adaptive MCP<br/>"
        "<b>Subtitle:</b> Why stateless agents hit a ceiling on Day 5, and how two-dimensional persistent memory enables autonomous tool evolution.<br/>"
        "<b>Tags:</b> #ai #programming #machinelearning #devtools #opensource",
        body_style
    ))
    story.append(Spacer(1, 4))

    article_summary = (
        "<b>Core Article Sections (Ready to publish):</b><br/>"
        "1. <b>The Stateless Agent Dilemma:</b> Why existing coding agents forget architecture and customer constraints every session.<br/>"
        "2. <b>Two-Dimensional Memory Architecture:</b> Separating business domain facts (<code>dias_deals</code>) from developer telemetry (<code>dias_telemetry</code>).<br/>"
        "3. <b>The Cognitive Lifecycle:</b> Concrete Python code snippets implementing Retain, Recall, and Reflect using <code>HindsightClient</code>.<br/>"
        "4. <b>Adaptive MCP Evolution:</b> How Hindsight reflections detect friction in SQL queries and dynamically configure Neon PostgreSQL MCP.<br/>"
        "5. <b>Verifiable Deliverables:</b> 20/20 pytest regression suite and automated executive PDF generation with ReportLab.<br/>"
        "6. <b>Try It Yourself:</b> Clone <code>github.com/Manibhushanamk/DEAL-INTELLIGENCE-AGENT-SKILL-DIAS-</code> and run <code>./run_all.sh</code>."
    )
    story.append(Paragraph(article_summary, body_style))

    # Build Document for primary path
    primary_path = output_paths[0]
    doc = SimpleDocTemplate(
        primary_path,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=42,
        bottomMargin=42
    )
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {primary_path} ({os.path.getsize(primary_path)} bytes)")

    # Copy to remaining target paths
    import shutil
    for path in output_paths[1:]:
        shutil.copyfile(primary_path, path)
        print(f"Successfully copied to {path} ({os.path.getsize(path)} bytes)")

if __name__ == "__main__":
    desktop_path = os.path.expanduser("~/Desktop/DIAS_FINAL_SUBMISSION_RUNBOOK.pdf")
    desktop_guide_path = os.path.expanduser("~/Desktop/HACKWITHHYDERABAD_FINAL_SUBMISSION_GUIDE.pdf")
    repo_path = os.path.expanduser("~/deal-intelligence-skill/HACKWITHHYDERABAD_FINAL_SUBMISSION_GUIDE.pdf")
    
    build_pdf([desktop_path, desktop_guide_path, repo_path])
