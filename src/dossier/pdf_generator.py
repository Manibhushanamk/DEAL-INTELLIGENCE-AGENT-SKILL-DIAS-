import os
from typing import Dict, Any, List, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

class PDFDossierGenerator:
    """
    Compiles high-resolution, C-level executive PDF deal dossiers using ReportLab.
    Includes Deal Health Scorecard, Multi-Vector Breakdown, Competitive Battlecard,
    Hindsight Memory Reflection, and Staged Workspace Action Plans.
    """
    def generate_dossier(
        self,
        output_filepath: str,
        account_name: str,
        deal_data: Dict[str, Any],
        analytics_summary: Dict[str, Any],
        battlecard: Optional[Dict[str, Any]] = None,
        hindsight_reflections: Optional[List[str]] = None
    ) -> str:
        """
        Builds and saves the executive PDF dossier to output_filepath.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)

        doc = SimpleDocTemplate(
            output_filepath,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Heading1'],
            fontSize=18,
            leading=22,
            textColor=colors.HexColor('#0F172A'),
            spaceAfter=8
        )
        h2_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontSize=12,
            leading=16,
            textColor=colors.HexColor('#1E3A8A'),
            spaceBefore=8,
            spaceAfter=4
        )
        body_style = ParagraphStyle(
            'BodyTextCustom',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor('#334155'),
            spaceAfter=3
        )
        table_cell = ParagraphStyle(
            'TableCell',
            parent=body_style,
            fontSize=8,
            leading=11
        )
        table_header = ParagraphStyle(
            'TableHeader',
            parent=body_style,
            fontName='Helvetica-Bold',
            fontSize=8,
            leading=11,
            textColor=colors.white
        )

        story = []

        # Top Banner
        banner = Table([[
            Paragraph("<b>DEAL INTELLIGENCE AGENT SKILL (DIAS) — EXECUTIVE DOSSIER</b>", ParagraphStyle('B1', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.white)),
            Paragraph(f"<b>STAGE: {deal_data.get('stage', 'PROPOSAL / NEGOTIATION').upper()}</b>", ParagraphStyle('B2', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.white, alignment=2))
        ]], colWidths=[380, 160])
        banner.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0F172A')),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(banner)
        story.append(Spacer(1, 8))

        # Title & Account Subtitle
        story.append(Paragraph(f"Executive Account Intelligence Dossier: <b>{account_name}</b>", title_style))
        story.append(Paragraph(f"Deal ID: <code>{deal_data.get('deal_id', 'DEAL-ACME-001')}</code> | Annual Contract Value (ACV): <b>{deal_data.get('amount', '$350,000')}</b> | Target Close: <b>{deal_data.get('close_date', 'Q4 2026')}</b>", body_style))
        story.append(Spacer(1, 6))

        # KPI Metric Cards
        health_score = analytics_summary.get('overall_health_score', 84.0)
        win_prob = analytics_summary.get('win_probability_pct', 78.0)
        health_tier = analytics_summary.get('health_tier', 'HEALTHY')
        color_hex = analytics_summary.get('color_hex', '#16A34A')

        kpi_table = Table([
            [
                Paragraph("<b>DEAL HEALTH SCORE</b>", ParagraphStyle('KL', fontSize=7.5, textColor=colors.HexColor('#64748B'))),
                Paragraph("<b>WIN PROBABILITY</b>", ParagraphStyle('KL', fontSize=7.5, textColor=colors.HexColor('#64748B'))),
                Paragraph("<b>HEALTH TIER</b>", ParagraphStyle('KL', fontSize=7.5, textColor=colors.HexColor('#64748B'))),
                Paragraph("<b>PRIMARY COMPETITOR</b>", ParagraphStyle('KL', fontSize=7.5, textColor=colors.HexColor('#64748B')))
            ],
            [
                Paragraph(f"<font size=16 color='{color_hex}'><b>{health_score} / 100</b></font>", body_style),
                Paragraph(f"<font size=16 color='#2563EB'><b>{win_prob}%</b></font>", body_style),
                Paragraph(f"<font size=12 color='{color_hex}'><b>{health_tier}</b></font>", body_style),
                Paragraph(f"<b>{deal_data.get('competitor', 'Gong.io / Legacy CRM')}</b>", body_style)
            ]
        ], colWidths=[135, 135, 135, 135])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(kpi_table)
        story.append(Spacer(1, 8))

        # Section 1: Multi-Vector Breakdown
        story.append(Paragraph("1. Multi-Vector Deal Diagnostic Health", h2_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#2563EB'), spaceAfter=4))
        
        vectors = analytics_summary.get("vectors", {})
        vec_data = [
            [Paragraph("Vector Dimension", table_header), Paragraph("Score", table_header), Paragraph("Max", table_header), Paragraph("Diagnostic Status", table_header)],
            [
                Paragraph("<b>Engagement Momentum</b>", table_cell),
                Paragraph(str(vectors.get("momentum", {}).get("score", 23.0)), table_cell),
                Paragraph("25.0", table_cell),
                Paragraph("High communication cadence; recent security review completed.", table_cell)
            ],
            [
                Paragraph("<b>Stakeholder Coverage</b>", table_cell),
                Paragraph(str(vectors.get("stakeholders", {}).get("score", 21.0)), table_cell),
                Paragraph("25.0", table_cell),
                Paragraph("VP of Security and Product Champion engaged; CFO pending final sign-off.", table_cell)
            ],
            [
                Paragraph("<b>Technical Alignment</b>", table_cell),
                Paragraph(str(vectors.get("technical_alignment", {}).get("score", 22.0)), table_cell),
                Paragraph("25.0", table_cell),
                Paragraph("Prerequisites met: SOC2 Type II validated, Okta SAML 2.0 integration verified.", table_cell)
            ],
            [
                Paragraph("<b>Commercial Feasibility</b>", table_cell),
                Paragraph(str(vectors.get("commercial_feasibility", {}).get("score", 18.0)), table_cell),
                Paragraph("25.0", table_cell),
                Paragraph("Procurement requested 15% discount concession; tiered license proposal recommended.", table_cell)
            ]
        ]
        t_vec = Table(vec_data, colWidths=[140, 50, 50, 300])
        t_vec.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(t_vec)
        story.append(Spacer(1, 8))

        # Section 2: Hindsight Memory Reflection
        story.append(Paragraph("2. Vectorize Hindsight Cloud Strategic Memory Synthesis", h2_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#2563EB'), spaceAfter=4))
        
        beliefs = hindsight_reflections or [
            "Account has explicit historical disclosures across: security, technical stack, budget, and competitor.",
            "Architecture and SSO compliance verification are critical closing prerequisites (AWS GovCloud + Okta SAML).",
            "Pricing & ROI justification is required before procurement execution.",
            "Active competitor evaluation detected (Gong.io); battlecard positioning required."
        ]
        for b in beliefs:
            story.append(Paragraph(f"• <b>Insight:</b> {b}", body_style))
        story.append(Spacer(1, 8))

        # Section 3: Competitive Battlecard
        if battlecard:
            story.append(Paragraph(f"3. Competitive Battlecard: vs. {battlecard.get('competitor_name', 'Competitor')}", h2_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#2563EB'), spaceAfter=4))
            
            b_data = [
                [Paragraph("Category", table_header), Paragraph("Strategic Analysis", table_header)],
                [Paragraph("<b>Core Weakness</b>", table_cell), Paragraph(battlecard.get("core_weakness", ""), table_cell)],
                [Paragraph("<b>Our Advantage</b>", table_cell), Paragraph(battlecard.get("our_advantage", ""), table_cell)],
                [Paragraph("<b>Trap-Setting Question</b>", table_cell), Paragraph(f"<i>\"{battlecard.get('trap_question', '')}\"</i>", table_cell)]
            ]
            t_b = Table(b_data, colWidths=[130, 410])
            t_b.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
                ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
                ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
                ('TOPPADDING', (0,0), (-1,-1), 3),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ]))
            story.append(t_b)
            story.append(Spacer(1, 8))

        # Section 4: Recommended Action Plan & Staging
        story.append(Paragraph("4. Recommended Action Plan & Human-in-the-Loop Workspace Staging", h2_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#2563EB'), spaceAfter=4))
        story.append(Paragraph("• <b>Gmail Follow-up Draft:</b> Staged executive summary highlighting SOC2 compliance and tiered proposal to VP of Security and Product Champion.", body_style))
        story.append(Paragraph("• <b>Google Calendar Executive Hold:</b> Staged tentative 30-minute procurement review hold for next Tuesday at 2:00 PM EST.", body_style))
        story.append(Paragraph("• <b>Adaptive MCP Next Step:</b> Neon PostgreSQL MCP ready for direct query of historical discount tiers and contract margins.", body_style))

        # Build PDF document
        doc.build(story)
        return output_filepath
