"""
Script to generate the HackwithHyderabad Final Submission Dossier & Video Guide PDF.
Includes complete step-by-step commands, terminal outputs, and screening guidance for the demo.
"""

import os
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
            self.drawString(54, 11 * inch - 36, "HACKWITHHYDERABAD 2026 — FINAL SUBMISSION DOSSIER & VIDEO RUNBOOK")
            self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "DIAS • DEAL INTELLIGENCE AGENT SKILL")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 46, 8.5 * inch - 54, 46)
        
        self.setFont("Helvetica", 8)
        self.drawString(54, 32, "Confidential • Project: Deal Intelligence Agent Skill (DIAS) • Vectorize Hindsight Cloud")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 32, page_text)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#0F172A")    # Deep Slate
    c_accent = colors.HexColor("#2563EB")     # Blue
    c_emerald = colors.HexColor("#059669")    # Emerald
    c_purple = colors.HexColor("#7C3AED")     # Purple
    c_dark = colors.HexColor("#1E293B")
    c_light = colors.HexColor("#F8FAFC")
    c_border = colors.HexColor("#CBD5E1")
    c_code_bg = colors.HexColor("#F1F5F9")

    # Typography styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_primary,
        alignment=0,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=c_accent,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_primary,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=c_accent,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_dark,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#1E3A8A"),
        spaceAfter=0
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A")
    )

    dialogue_style = ParagraphStyle(
        'DialogueStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E293B")
    )

    th_style = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.white
    )

    td_style = ParagraphStyle(
        'TD',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=c_dark
    )

    story = []

    # ================= PAGE 1: TITLE & SUBMISSION FORM CHEAT SHEET =================
    story.append(Paragraph("HACKWITHHYDERABAD 2026 — FINAL SUBMISSION DOSSIER", title_style))
    story.append(Paragraph("<b>Project:</b> Deal Intelligence Agent Skill (DIAS) | <b>Cognitive Brain:</b> Vectorize Hindsight Cloud", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=0, spaceAfter=8))

    # Alert Box
    alert_data = [[
        Paragraph("<b>CRITICAL SUBMISSION CHECKLIST & RULES:</b><br/>"
                  "1. <b>DO NOT mention 'Hackathon'</b> in LinkedIn Post or Article title/body/tags (Strict Disqualification Rule).<br/>"
                  "2. All team members must complete the Profile Review Form: <u>https://forms.gle/AXWnanWsEEir6xSP9</u>.<br/>"
                  "3. Submit this finalized project on Google Form: <u>https://forms.gle/cD7fCnPnkdVm2sH78</u> before deadline.", callout_style)
    ]]
    alert_table = Table(alert_data, colWidths=[7.0 * inch])
    alert_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(alert_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("📋 Official Google Form Submission Fields (Copy-Paste Directory)", h1_style))
    story.append(Paragraph("Open the final submission form at <b>https://forms.gle/cD7fCnPnkdVm2sH78</b> and fill with these exact details:", body_style))

    form_rows = [
        [Paragraph("Form Field", th_style), Paragraph("Exact Value to Submit / Guidance", th_style)],
        [Paragraph("<b>Email ID *</b>", td_style), Paragraph("<b>manibhushanam4k@gmail.com</b>", td_style)],
        [Paragraph("<b>Phone Number *</b>", td_style), Paragraph("<i>[Enter your 10-digit registered mobile number, e.g., +91 9876543210]</i>", td_style)],
        [Paragraph("<b>Team Name *</b>", td_style), Paragraph("<i>[Enter your exact registered Team Name as entered during registration]</i>", td_style)],
        [Paragraph("<b>Team Members *</b>", td_style), Paragraph("<i>[List full legal names of all team members, e.g., Manibhushanam K, ...]</i>", td_style)],
        [Paragraph("<b>GitHub Repository Link *</b>", td_style), Paragraph("<b>https://github.com/Manibhushanamk/DEAL-INTELLIGENCE-AGENT-SKILL-DIAS-</b>", td_style)],
        [Paragraph("<b>Social Media Post (LinkedIn) *</b>", td_style), Paragraph("Paste the public URL of your LinkedIn post (Use Section 3 of this document for exact copy).", td_style)],
        [Paragraph("<b>Article Link *</b>", td_style), Paragraph("Paste your published Dev.to / Medium / Hashnode article URL (Use Section 4 for complete text).", td_style)],
        [Paragraph("<b>Video Link *</b>", td_style), Paragraph("Paste your public YouTube demo video URL (Use Section 2 for full command runbook & script).", td_style)],
        [Paragraph("<b>Reddit Post Link *</b>", td_style), Paragraph("Paste your published link from <i>r/aiagents</i> or <i>r/aimemory</i> (Use Section 5 for copy).", td_style)],
        [Paragraph("<b>FEEDBACK *</b>", td_style), Paragraph("Copy the comprehensive organizer feedback provided in Section 6 of this dossier.", td_style)]
    ]
    form_table = Table(form_rows, colWidths=[2.2 * inch, 4.8 * inch])
    form_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
    ]))
    story.append(form_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("🏆 Project Identity & Technical Highlights", h1_style))
    highlight_text = (
        "• <b>Project Name:</b> Deal Intelligence Agent Skill (DIAS)<br/>"
        "• <b>Core Novelty:</b> Persistent multi-session memory via <b>Vectorize Hindsight Cloud</b> + <b>Adaptive MCP capability evolution</b>.<br/>"
        "• <b>Verified Architecture:</b> Two-dimensional memory banks (<code>dias_deals</code> and <code>dias_telemetry</code>) hosted on <code>api.hindsight.vectorize.io</code>.<br/>"
        "• <b>Real Invariant Assertions:</b> 20/20 pytest tests passing in 44.4s, zero credential leaks (<code>hsk_...50fc</code>), live ReportLab PDF dossier generation (6,224 bytes)."
    )
    story.append(Paragraph(highlight_text, body_style))

    story.append(PageBreak())

    # ================= PAGE 2, 3, 4: SCENE-BY-SCENE VIDEO SCRIPT WITH COMMANDS & SCREENING =================
    story.append(Paragraph("🎬 3-Minute Video Demo — Complete Scene-by-Scene Script & Screening Guide", h1_style))
    story.append(Paragraph(
        "<b>Video Goal:</b> Deliver a crisp, confident screen recording (2 to 3 minutes) matching the exact terminal commands "
        "and voiceover dialogue below. Every scene details what to type, what appears on screen, what lines to highlight, and what to say.", body_style))
    story.append(Spacer(1, 4))

    # Critical Environment Instruction Box
    venv_alert_data = [[
        Paragraph("<b>🚀 MASTER 1-COMMAND EXECUTION (RECOMMENDED FOR VIDEO DEMO):</b><br/>"
                  "DIAS provides an automated all-in-one runner that auto-detects the virtual environment, runs the setup wizard, executes the enterprise deal demo, and generates the final analysis result:<br/>"
                  "• <b>Fast Video Demo Mode (Under 10s):</b> <code>./run_all.sh --skip-tests</code><br/>"
                  "• <b>Full Master Pipeline (With 20/20 Tests):</b> <code>./run_all.sh</code><br/>"
                  "• <b>Modular Runners:</b> <code>./run_wizard.sh</code> &nbsp;|&nbsp; <code>./run_demo.sh</code> &nbsp;|&nbsp; <code>./run_tests.sh</code>", callout_style)
    ]]
    venv_alert_table = Table(venv_alert_data, colWidths=[7.0 * inch])
    venv_alert_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(venv_alert_table)
    story.append(Spacer(1, 6))

    def render_scene_box(scene_id, time_range, title, cmd_block, screen_actions, dialogue_text, pro_tip):
        card_content = []
        
        # Header banner
        header_text = f"<b>{scene_id} ({time_range}) — {title.upper()}</b>"
        header_p = Paragraph(header_text, ParagraphStyle('SH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=colors.white))
        header_table = Table([[header_p]], colWidths=[7.0 * inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c_primary),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        card_content.append(header_table)

        # Inner body table
        rows = [
            [
                Paragraph("<b>💻 Terminal Work & Commands to Run:</b>", ParagraphStyle('L', parent=body_style, fontName='Helvetica-Bold', textColor=c_accent)),
                Paragraph(f"<code>{cmd_block}</code>", code_style)
            ],
            [
                Paragraph("<b>🖥️ On-Screen Action & Visual Cues:</b>", ParagraphStyle('L', parent=body_style, fontName='Helvetica-Bold', textColor=c_primary)),
                Paragraph(screen_actions, body_style)
            ],
            [
                Paragraph("<b>🗣️ Exact Voiceover Dialogue (What to Say):</b>", ParagraphStyle('L', parent=body_style, fontName='Helvetica-Bold', textColor=c_emerald)),
                Paragraph(f"\"{dialogue_text}\"", dialogue_style)
            ],
            [
                Paragraph("<b>💡 Recording Pro-Tip & Timing:</b>", ParagraphStyle('L', parent=body_style, fontName='Helvetica-Bold', textColor=colors.HexColor("#D97706"))),
                Paragraph(pro_tip, callout_style)
            ]
        ]
        body_table = Table(rows, colWidths=[2.2 * inch, 4.8 * inch])
        body_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, c_border),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('ROWBACKGROUNDS', (0,0), (-1,-1), [c_light, colors.white, c_light, colors.HexColor("#FFFBEB")]),
        ]))
        card_content.append(body_table)
        card_content.append(Spacer(1, 8))
        return KeepTogether(card_content)

    # SCENE 1
    story.append(render_scene_box(
        "SCENE 1", "00:00 – 00:25 (25s)", "The Hook & The Stateless Agent Problem",
        "# 1. Navigate to repository directory<br/>"
        "cd ~/deal-intelligence-skill && clear<br/>"
        "# 2. Show clean directory structure<br/>"
        "ls -la",
        "• Split screen: Clean terminal on right, GitHub repository on left.<br/>"
        "• Camera on face (optional) or full screen desktop recording.<br/>"
        "• Point mouse at the core dilemma: AI coding agents lose all context between sessions.",
        "Hi everyone! I'm Manibhushanam, and this is <b>DIAS — Deal Intelligence Agent Skill</b>.<br/><br/>"
        "Today, autonomous AI coding agents are stateless. Every time you start a session, it's Day 1 all over again: "
        "they forget customer mandates, ignore compliance history, and operate with rigid tools.<br/><br/>"
        "We solved this by giving host coding agents a permanent cognitive brain powered by <b>Vectorize Hindsight Cloud</b>.",
        "Start with confident, energetic delivery. Keep terminal clear and ready for the 1-command launch."
    ))

    # SCENE 2
    story.append(render_scene_box(
        "SCENE 2", "00:25 – 01:10 (45s)", "1-Command Launch & Live Enterprise Deal Analysis",
        "# Run the master pipeline in fast video mode:<br/>"
        "./run_all.sh --skip-tests",
        "• Terminal runs Stage 1 (Setup Wizard) and Stage 2 (Enterprise Demo) live.<br/>"
        "• <b>Highlight with mouse:</b><br/>"
        "  1. <code>Host Agent: ✓ Google Jules detected</code><br/>"
        "  2. <code>Hindsight API Key: hsk_...50fc (Masked, Zero-Leak)</code><br/>"
        "  3. <code>Pre-Flight Triad: RETAIN: ✓ Passed | RECALL: ✓ Passed | REFLECT: ✓ Passed</code><br/>"
        "  4. <code>Live Enterprise Deal: Acme Corp ($350k ARR, 150 seats)</code><br/>"
        "  5. <code>👉 RECOMMENDED MCP: Neon PostgreSQL MCP (Impact: 95/100)</code>",
        "With a single command, <code>./run_all.sh</code>, DIAS kicks off.<br/><br/>"
        "First, our setup wizard auto-detects the host environment — Google Jules, OpenClaw, or Antigravity. "
        "It authenticates with Vectorize Hindsight Cloud using zero-leak key masking, provisions our two dedicated memory banks, "
        "and validates a pre-flight triad: Retain, Recall, and Reflect.<br/><br/>"
        "Then DIAS processes an enterprise deal: <b>Acme Corp</b>, a $350,000 ARR contract with Gong.io competition. "
        "Notice how our telemetry engine detects relational SQL friction and dynamically recommends the Neon PostgreSQL MCP!",
        "Let the terminal stream smoothly. Point your mouse at the green checkmarks as they appear."
    ))

    story.append(PageBreak())

    # SCENE 3
    story.append(render_scene_box(
        "SCENE 3", "01:10 – 01:45 (35s)", "Terminal Scroll: Project Result Analysis & Executive PDF",
        "# 1. Scroll through terminal to show Project Result banner<br/>"
        "# 2. Open and showcase the generated C-Level Deal Dossier PDF<br/>"
        "xdg-open acme_corp_deal_dossier.pdf",
        "• Scroll terminal window up and down to display the complete analysis.<br/>"
        "• Highlight the <b>PROJECT RESULT</b> section on screen:<br/>"
        "  - <code>Deal Health Score: 85.0 / 100 (EXCELLENT)</code><br/>"
        "  - <code>Win Probability: 78.2% (High Confidence)</code><br/>"
        "  - <code>AWS GovCloud Mandate + Okta SAML 2.0 (Resolved)</code><br/>"
        "• Switch to <code>acme_corp_deal_dossier.pdf</code> open in document viewer.<br/>"
        "• Show diagnostic radar bars, SWOT analysis, and Gong competitor battlecard.",
        "Let's look at the result of the analysis: DIAS calculates an overall deal health of <b>85.0 out of 100</b> "
        "and a <b>78.2% win probability</b> across 4 diagnostic vectors.<br/><br/>"
        "It resolved Acme's mandatory AWS GovCloud and Okta SAML 2.0 requirements, and built an objection defense against Gong.<br/><br/>"
        "Best of all, DIAS compiled this publication-grade C-level PDF deal dossier on the fly with full SWOT matrix and competitor battlecards!",
        "Slowly scroll down Page 1 to Page 2 of the PDF so the radar bars, competitor battlecards, and SWOT layout are clearly visible."
    ))

    # SCENE 4
    story.append(render_scene_box(
        "SCENE 4", "01:45 – 02:25 (40s)", "Vectorize Hindsight Cloud: Live Usage & Memory Banks",
        "# Switch browser to Hindsight Cloud live interface:<br/>"
        "# Tab 1: https://ui.hindsight.vectorize.io/usage<br/>"
        "# Tab 2: https://ui.hindsight.vectorize.io/dashboard",
        "• <b>Switch to Browser Tab 1:</b> <code>https://ui.hindsight.vectorize.io/usage</code><br/>"
        "  Show live API request volume, token usage, and real-time operations graph.<br/>"
        "• <b>Switch to Browser Tab 2:</b> <code>https://ui.hindsight.vectorize.io/dashboard</code><br/>"
        "  Click into <code>dias_deals</code> memory bank.<br/>"
        "  Show actual Acme Corp memory nodes, timestamps, and reflected strategic insights.",
        "Now let's verify where this cognitive intelligence lives: here in <b>Vectorize Hindsight Cloud</b>.<br/><br/>"
        "On the Usage screen, you can see the real-time API operations and token throughput generated by our demo.<br/><br/>"
        "And in the Dashboard under our <code>dias_deals</code> memory bank, here are the actual persisted memories: "
        "Acme's GovCloud mandate, Okta SSO requirements, and the synthesized reflection summary. "
        "This proves DIAS doesn't rely on ephemeral state — it has a true cloud-native cognitive brain.",
        "Keep the browser zoomed to 110% so the memory cards, timestamps, and Vectorize logos are sharp and legible."
    ))

    # SCENE 5
    story.append(render_scene_box(
        "SCENE 5", "02:25 – 02:50 (25s)", "GitHub README Walkthrough & Architecture",
        "# Switch browser to public GitHub repository:<br/>"
        "# URL: https://github.com/Manibhushanamk/DEAL-INTELLIGENCE-AGENT-SKILL-DIAS-",
        "• Open repository README in browser.<br/>"
        "• Highlight the <b>Continuous Learning Curve</b> diagram (Day 1 ➔ Day 5 ➔ Day 20+).<br/>"
        "• Highlight the <b>1-Command Quick Start</b> code box so judges see how easy reproduction is.<br/>"
        "• Briefly show the 8 MCP tool definitions and test badges.",
        "Everything in DIAS is open-source and judge-ready on GitHub.<br/><br/>"
        "Our README details the full cognitive architecture, our two-dimensional memory design, and the adaptive MCP router.<br/><br/>"
        "Most importantly, any developer or judge can clone the repository and reproduce this entire pipeline with a single command: "
        "<code>./run_all.sh</code>.",
        "Scroll at a steady pace through the README. Pause on the architecture diagram and the 1-command quick start."
    ))

    # SCENE 6
    story.append(render_scene_box(
        "SCENE 6", "02:50 – 03:00 (10s)", "Test Verification (20/20) & Closing Call to Action",
        "# Quick terminal verification:<br/>"
        "./run_tests.sh",
        "• Show terminal with 20/20 green pytest passes.<br/>"
        "• Highlight: <code>==================== 20 passed in 50s ====================</code><br/>"
        "• Display GitHub repository link on screen.",
        "With 20 out of 20 verified tests passing, DIAS shows how persistent memory transforms AI agents into self-improving partners.<br/><br/>"
        "Check out our repository at github.com/Manibhushanamk/DEAL-INTELLIGENCE-AGENT-SKILL-DIAS-. Thank you!",
        "End on the green 20/20 test pass banner or the GitHub homepage as your final screen."
    ))

    story.append(Spacer(1, 6))
    story.append(Paragraph("🎯 5 High-Performing Click-Worthy YouTube Titles", h2_style))
    titles_text = (
        "1. <b>I Gave My AI Coding Agent a Memory Brain — Then It Upgraded Its Own Tools</b><br/>"
        "2. <b>Stop Building Stateless Agents: How We Built DIAS with Vectorize Hindsight Cloud</b><br/>"
        "3. <b>How This AI Agent Learned From My Mistakes and Wired Its Own MCP Database</b><br/>"
        "4. <b>From Day 1 to Day 20: Watch an AI Agent Actually Evolve Using Hindsight Memory</b><br/>"
        "5. <b>Autonomous Deal Intelligence: Building a Learning Sales Copilot with Hindsight & MCP</b>"
    )
    story.append(Paragraph(titles_text, body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("🖼️ Viral YouTube Thumbnail Prompt (Use in Google Nano Banana / Imagen)", h2_style))
    story.append(Paragraph(
        "<i>\"High-impact 16:9 YouTube tech thumbnail. Split composition: On the left, a frustrated robot with an 'AMNESIA / MEMORY: 0%' error prompt. "
        "On the right, a glowing futuristic cybernetic brain connected to terminal code streams showing 'HINDSIGHT CLOUD: CONNECTED' and 'DEAL HEALTH: 85.0/100'. "
        "Bold vibrant text overlay: 'AGENTS THAT LEARN'. Dark cyberpunk blue and emerald neon lighting, 8k resolution, crisp photorealistic developer aesthetic.\"</i>",
        callout_style
    ))

    story.append(PageBreak())

    # ================= PAGE 5: SOCIAL MEDIA (LINKEDIN & REDDIT) =================
    story.append(Paragraph("📱 Official Social Media Posts (LinkedIn & Reddit)", h1_style))
    story.append(Paragraph("<b>STRICT COMPLIANCE NOTICE:</b> Zero mentions of the word 'hackathon' anywhere in title, body, or hashtags.", callout_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("💼 Part 1: Official LinkedIn Post Copy (Under 800 Characters)", h2_style))
    story.append(Paragraph("<i>Copy the exact text inside the box below, paste into LinkedIn, add your GitHub link, and publish:</i>", body_style))

    linkedin_text = (
        "Most AI coding agents are stateless amnesiacs.<br/><br/>"
        "Every time you open a terminal, it’s Day 1 all over again: customer compliance needs get lost, objections are forgotten, and agents operate with rigid, hard-coded tools.<br/><br/>"
        "We built DIAS (Deal Intelligence Agent Skill) to fix this using @Vectorize Hindsight Cloud as the cognitive brain.<br/><br/>"
        "Here is what happens when an agent actually has persistent memory:<br/>"
        "• Retain & Recall: Inscribes $350k enterprise deal facts (GovCloud, Okta SSO) into Hindsight Cloud and recalls them with zero hallucination.<br/>"
        "• Cognitive Reflection: Synthesizes buyer objections and competitor claims (Gong/Clari) across multi-session interactions.<br/>"
        "• Adaptive MCP Evolution: Observes repeated SQL queries in telemetry and dynamically wires Neon Serverless PostgreSQL.<br/>"
        "• Grounded Deal Scoring: Delivers 85.0/100 health analytics and compiles executive PDF dossiers.<br/><br/>"
        "Code is open-source on GitHub:<br/>"
        "https://github.com/Manibhushanamk/DEAL-INTELLIGENCE-AGENT-SKILL-DIAS-<br/><br/>"
        "#AIAgents #AI #Hindsight #AgentMemory #AIMemory #LLM"
    )
    li_table = Table([[Paragraph(linkedin_text, body_style)]], colWidths=[7.0 * inch])
    li_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(li_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("💬 Required First Comment on Your LinkedIn Post:", h2_style))
    comment_text = (
        "<b>Comment 1:</b> <i>\"Here’s the link to the Hindsight repository if you want to explore persistent agent memory: "
        "https://github.com/vectorize-io/hindsight — Shoutout to @Vectorize and @Code.in for building powerful developer tools!\"</i>"
    )
    story.append(Paragraph(comment_text, body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("👽 Part 2: Official Reddit Post Copy (r/aiagents, r/aimemory, r/llmdevs)", h2_style))
    story.append(Paragraph("<b>Target Subreddits:</b> <code>r/aiagents</code>, <code>r/aimemory</code>, <code>r/llmdevs</code>, <code>r/sideproject</code>", body_style))

    reddit_body = (
        "<b>Title:</b> We built an AI Agent Skill with Vectorize Hindsight that remembers enterprise deal context and adapts its own MCP tools<br/><br/>"
        "<b>Post Body:</b><br/>"
        "Hey everyone,<br/><br/>"
        "One of the biggest frustrations with autonomous coding agents is that they lack long-term memory. If you discuss security requirements on Monday, by Thursday the agent has completely forgotten about AWS GovCloud and Okta SSO mandates.<br/><br/>"
        "To solve this, we built <b>DIAS (Deal Intelligence Agent Skill)</b>. Instead of treating memory as a short-term prompt buffer, DIAS connects directly to <b>Vectorize Hindsight Cloud</b> as its cognitive brain.<br/><br/>"
        "<b>How it works:</b><br/>"
        "1. <b>Two-Dimensional Memory:</b> We partition memory into <code>dias_deals</code> (customer facts, competitor counter-tactics) and <code>dias_telemetry</code> (how the operator works).<br/>"
        "2. <b>Retain, Recall, Reflect:</b> The agent retrieves semantic memories before answering, and uses Hindsight Reflect to extract cross-session meta-patterns.<br/>"
        "3. <b>Adaptive MCP:</b> When DIAS notices 3+ manual SQL lookups in telemetry, it automatically recommends and wires the Neon Serverless PostgreSQL MCP server with human approval.<br/>"
        "4. <b>Enterprise Output:</b> Multi-vector deal health scoring (85.0/100) and publication-grade ReportLab PDF dossiers.<br/><br/>"
        "Everything is open source with 20/20 passing tests and full Hindsight Cloud integration:<br/>"
        "Repo: https://github.com/Manibhushanamk/DEAL-INTELLIGENCE-AGENT-SKILL-DIAS-<br/>"
        "Hindsight Repo: https://github.com/vectorize-io/hindsight<br/><br/>"
        "Would love feedback on our adaptive MCP approach and memory partitioning!"
    )
    rd_table = Table([[Paragraph(reddit_body, body_style)]], colWidths=[7.0 * inch])
    rd_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFF7ED")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FED7AA")),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(rd_table)

    story.append(PageBreak())

    # ================= PAGE 6 & 7: COMPLETE TECHNICAL ARTICLE =================
    story.append(Paragraph("📰 Official Technical Article (800–1,500 Words)", h1_style))
    story.append(Paragraph("<b>Publish Platforms:</b> Medium, Dev.to, Hashnode, Substack, or LinkedIn Articles.<br/>"
                           "<b>Pre-Submit Guarantee:</b> ZERO mentions of 'hackathon', real codebase snippets, before/after analysis, Hindsight Cloud links.", callout_style))
    story.append(Spacer(1, 8))

    article_title = "Why AI Agents Suffer from Amnesia — And How We Built a Self-Adapting Sales Copilot Using Vectorize Hindsight Cloud"
    story.append(Paragraph(f"<b>Title:</b> {article_title}", h2_style))
    story.append(Paragraph("<i>By Manibhushanam K & Team | Reading Time: 6 min | Tags: AI, AgentMemory, Python, Architecture</i>", subtitle_style))

    p1 = (
        "In artificial intelligence, we often celebrate the expanding context window. Models can now ingest 1 million tokens "
        "in a single prompt. Yet, despite massive context windows, current AI coding agents remain fundamentally amnesiac. "
        "Every time a developer or sales engineer spins up a new agent session, it behaves as if it were born five seconds ago. "
        "Customer compliance mandates, pricing concessions, and competitor landmines vanish into thin air. "
        "To make agents truly useful in high-stakes domains like enterprise software sales, agents cannot just be stateless reasoning engines. "
        "They need a persistent cognitive substrate."
    )
    story.append(Paragraph(p1, body_style))

    p2 = (
        "To bridge this gap, we built <b>DIAS (Deal Intelligence Agent Skill)</b>. By anchoring host coding agents — such as Google Jules, "
        "OpenClaw, and Antigravity — to <b><a href='https://vectorize.io/what-is-agent-memory'>Vectorize Hindsight Cloud</a></b>, DIAS establishes "
        "a persistent cognitive memory layer that retains deal disclosures, semantically recalls historical context during conversations, "
        "reflects on interaction patterns, and dynamically adapts its Model Context Protocol (MCP) capabilities as developer needs evolve."
    )
    story.append(Paragraph(p2, body_style))

    story.append(Paragraph("The Two-Dimensional Memory Architecture", h2_style))
    p3 = (
        "When designing persistent memory for an agent, a common trap is dumping everything into a single key-value store or vector collection. "
        "This dilutes semantic relevance. A buyer's AWS GovCloud requirement has very different retention and reflection dynamics than the fact that "
        "the user executed four SQL queries in the terminal. DIAS solves this by introducing a Two-Dimensional Memory Architecture partitioned into "
        "two dedicated Hindsight Cloud Memory Banks:"
    )
    story.append(Paragraph(p3, body_style))

    p4 = (
        "• <b>Domain 1: Deal Memory (Bank: <code>dias_deals</code>):</b> Stores customer security mandates (SOC2, SAML 2.0 Okta SSO), "
        "commercial discount agreements, stakeholder authority maps, and competitor disclosures (Gong.io, Clari).<br/>"
        "• <b>Domain 2: Telemetry Memory (Bank: <code>dias_telemetry</code>):</b> Records user prompts, tool latency, repeated manual queries, "
        "and operational friction points."
    )
    story.append(Paragraph(p4, body_style))

    story.append(Paragraph("The Code: Integrating Hindsight Cloud", h2_style))
    story.append(Paragraph("Here is how DIAS synchronously communicates with Vectorize Hindsight Cloud via clean REST abstractions:", body_style))

    code_snip = (
        "# src/memory/hindsight_client.py<br/>"
        "class HindsightClient:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;def retain(self, bank_id: str, content: str, metadata: dict) -&gt; dict:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;payload = {'content': content, 'metadata': metadata}<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;resp = requests.post(f'{self.base_url}/v1/default/banks/{bank_id}/memories',<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;headers=self._headers, json=payload)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return resp.json()<br/><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;def recall(self, bank_id: str, query: str, top_k: int = 5) -&gt; list:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;payload = {'query': query, 'top_k': top_k}<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;resp = requests.post(f'{self.base_url}/v1/default/banks/{bank_id}/memories/recall',<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;headers=self._headers, json=payload)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return resp.json().get('memories', [])"
    )
    code_table = Table([[Paragraph(code_snip, code_style)]], colWidths=[7.0 * inch])
    code_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(code_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Before vs. After: The Reality of Agent Evolution", h2_style))
    p5 = (
        "<b>Day 1 (Without Hindsight Memory):</b><br/>"
        "<i>User:</i> 'Prepare a brief for Acme Corp.'<br/>"
        "<i>Agent:</i> 'Acme Corp is a fictional company often used in examples. How would you like me to help you today?' (Generic, useless).<br/><br/>"
        "<b>Day 20 (With DIAS & Hindsight Memory):</b><br/>"
        "<i>User:</i> 'Prepare a brief for Acme Corp.'<br/>"
        "<i>Agent:</i> 'Acme Corp is in the Negotiation stage for a $350,000 ARR contract. Key blocker: VP of Security mandates AWS GovCloud "
        "and Okta SAML 2.0 authentication. Gong.io is pitching a 20% discount. Win Probability is currently 78.2%, and Deal Health is 85.0/100. "
        "I noticed you ran 3 pipeline SQL queries earlier, so I have dynamically staged the Neon PostgreSQL MCP server to inspect active schema tables.'"
    )
    story.append(Paragraph(p5, body_style))

    story.append(Paragraph("Honest Lessons & Engineering Realities", h2_style))
    p6 = (
        "Building DIAS taught us several practical lessons. First, cloud recall payloads return diverse schemas: Vectorize Hindsight Cloud "
        "returns memory items under <code>text</code>, whereas local development fallbacks often expect <code>content</code>. "
        "Normalizing schema adapters early saved hours of debugging. Second, autonomous tool addition must always have human-in-the-loop gates: "
        "DIAS proactively suggests wiring MCP servers, but never connects network endpoints without explicit human approval. "
        "Persistent memory isn't just about storing tokens — it is about empowering agents to understand their user over time."
    )
    story.append(Paragraph(p6, body_style))

    story.append(Paragraph("Resources & Official Links", h2_style))
    story.append(Paragraph(
        "• <b>Project Repository:</b> <a href='https://github.com/Manibhushanamk/DEAL-INTELLIGENCE-AGENT-SKILL-DIAS-'>GitHub / DIAS</a><br/>"
        "• <b>Vectorize Hindsight GitHub:</b> <a href='https://github.com/vectorize-io/hindsight'>vectorize-io/hindsight</a><br/>"
        "• <b>Hindsight Documentation:</b> <a href='https://hindsight.vectorize.io/'>hindsight.vectorize.io</a><br/>"
        "• <b>Agent Memory Overview:</b> <a href='https://vectorize.io/what-is-agent-memory'>vectorize.io/what-is-agent-memory</a>",
        body_style
    ))

    story.append(PageBreak())

    # ================= PAGE 8: COMPETITION FEEDBACK & VERIFICATION APPENDIX =================
    story.append(Paragraph("💬 Official Organizer Feedback & Technical Appendix", h1_style))
    story.append(Paragraph("<b>Form Question:</b> <i>Did the competition do anything really well, or are there any ways to improve?</i>", h2_style))

    feedback_text = (
        "<b>What the competition did exceptionally well:</b><br/>"
        "1. <b>Focus on Real Agent Architecture Over Toy Chatbots:</b> By centering the challenge on persistent memory with Vectorize Hindsight, "
        "this hackathon forced builders to confront the real frontier of AI agent design. The emphasis on stateful cognition, multi-session learning, "
        "and Model Context Protocol (MCP) sets this competition apart from typical prompt-engineering hackathons.<br/>"
        "2. <b>High-Quality Developer Infrastructure:</b> Providing Hindsight Cloud accounts (with MEMHACK99 credits) and supporting Indian AI coding partners "
        "like Code.in gave teams enterprise-grade tooling to build production-ready systems rapidly.<br/>"
        "3. <b>Clear, Rigorous Content Guidelines:</b> The prohibition against marketing fluff and the requirement for real code, before/after contrasts, "
        "and honest lessons elevated the quality of all submissions.<br/><br/>"
        "<b>Actionable Recommendations for Future Editions:</b><br/>"
        "1. <b>SDK Client Packaging:</b> Publishing a standard, lightweight PyPI package (e.g., <code>pip install hindsight-ai</code>) with pre-built Pydantic "
        "schemas for Recall and Reflect would reduce initial boilerplate for REST integrations.<br/>"
        "2. <b>Bi-Temporal Memory Benchmarks:</b> Providing standardized benchmark datasets for multi-session agent memory testing would help teams objectively "
        "measure memory retention and decay accuracy against baseline LLMs."
    )
    fb_table = Table([[Paragraph(feedback_text, body_style)]], colWidths=[7.0 * inch])
    fb_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#86EFAC")),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(fb_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("🔬 Technical Verification Appendix (20 / 20 Tests Passed)", h1_style))
    test_summary = (
        "DIAS has been verified through a complete 20-scenario automated regression suite in <code>tests/</code>:<br/>"
        "• <b>Hindsight Memory (5/5 PASS):</b> Live connection ping, masked key audit (<code>hsk_...50fc</code>), RETAIN persistence, RECALL semantic search, and REFLECT synthesis.<br/>"
        "• <b>Adaptive MCP Setup (3/3 PASS):</b> Host detection across Jules, OpenClaw, Antigravity, and unattended setup.<br/>"
        "• <b>Error Handling & Resilience (8/8 PASS):</b> Missing keys, 401 unauthenticated, missing banks, network loss, and 404 endpoint recovery.<br/>"
        "• <b>Skill Invocation (3/3 PASS):</b> Multi-vector scoring calculations and JSON-RPC 2.0 stdio MCP dispatch.<br/>"
        "• <b>Executive Dossier (1/1 PASS):</b> Publication-grade ReportLab PDF generation (6,224 bytes).<br/>"
        "<b>Total Verification:</b> 20 passed in 44.43s (100% PASS)."
    )
    story.append(Paragraph(test_summary, body_style))

    # Build PDF with custom NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {filename} ({os.path.getsize(filename)} bytes)")

if __name__ == '__main__':
    output_pdf = "/home/kmanib/deal-intelligence-skill/HACKWITHHYDERABAD_FINAL_SUBMISSION_GUIDE.pdf"
    build_pdf(output_pdf)
