#!/usr/bin/env python3
"""
Generate Legal Timeline PDF for Whistleblower Retaliation Case
"""

import os
from pathlib import Path
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Image as RLImage, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import HexColor
from datetime import datetime

def create_legal_pdf():
    """Create comprehensive legal timeline PDF"""

    # Setup paths
    evidence_dir = Path("/Users/ugochi141/Desktop/CRITICAL_EVIDENCE_QUICK")
    output_pdf = Path("/Users/ugochi141/Desktop/WHISTLEBLOWER_TIMELINE_EVIDENCE.pdf")

    # Create PDF document
    doc = SimpleDocTemplate(str(output_pdf), pagesize=letter,
                          topMargin=0.75*inch, bottomMargin=0.75*inch,
                          leftMargin=0.5*inch, rightMargin=0.5*inch)

    # Setup styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle',
                                parent=styles['Heading1'],
                                fontSize=24,
                                textColor=HexColor('#000080'),
                                spaceAfter=30,
                                alignment=TA_CENTER)

    subtitle_style = ParagraphStyle('CustomSubtitle',
                                   parent=styles['Heading2'],
                                   fontSize=18,
                                   textColor=HexColor('#800000'),
                                   spaceAfter=20,
                                   alignment=TA_LEFT)

    body_style = ParagraphStyle('CustomBody',
                               parent=styles['BodyText'],
                               fontSize=12,
                               leading=16,
                               spaceAfter=12)

    # Build story
    story = []

    # Cover page
    story.append(Paragraph("WHISTLEBLOWER RETALIATION TIMELINE", title_style))
    story.append(Paragraph("Largo Laboratory - Kaiser Permanente", subtitle_style))
    story.append(Spacer(1, 0.5*inch))

    story.append(Paragraph("<b>Case Summary:</b>", body_style))
    story.append(Paragraph(
        "This document presents chronological evidence of retaliation against Ugochi L. Ndubuisi "
        "for protected whistleblowing activity regarding systemic performance issues affecting patient safety "
        "at Largo Laboratory.", body_style))

    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Key Pattern:</b>", body_style))
    story.append(Paragraph(
        "• July 14: Director orders investigation<br/>"
        "• September 29: Analysis provided and acknowledged<br/>"
        "• October 3: Same analysis shared with staff (protected activity)<br/>"
        "• October 3: Four censorship demands in 8 hours<br/>"
        "• October 8: Final Written Warning (first discipline in 9 months)",
        body_style))

    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Maryland OSHA Deadline:</b> November 7, 2025", body_style))
    story.append(Paragraph(f"<b>Document Generated:</b> {datetime.now().strftime('%B %d, %Y')}", body_style))

    story.append(PageBreak())

    # Critical events with evidence
    critical_events = [
        {
            "title": "JULY 14, 2025 - INVESTIGATION ORDERED",
            "description": "Director Nathaniel Burmeister orders investigation into second shift performance. "
                         "Metrics shared: 57%, 70%, 75%, 66% performance rates.",
            "files": ["July_14_Investigation_01_Screenshot 2025-10-03 at 8.35.06 PM.png",
                     "July_14_Investigation_02_Screenshot 2025-10-07 at 4.06.23 PM.png"]
        },
        {
            "title": "SEPTEMBER 29, 2025 - ANALYSIS PROVIDED",
            "description": "Ugochi provides comprehensive analysis: 'Culture issue runs deeper than individual "
                         "performance.' References Level 3 Trauma hospital requirements. "
                         "Director acknowledges: 'I see the issue with staffing.'",
            "files": ["Sept_29_Analysis_01_Screenshot 2025-10-14 at 8.56.10 AM.png",
                     "Sept_29_Analysis_02_Screenshot 2025-10-07 at 4.06.55 PM.png"]
        },
        {
            "title": "OCTOBER 3, 2025 - WHISTLEBLOWING ACTIVITY",
            "description": "8:21 AM: Ugochi shares analysis with staff, including 41.23% failure rate data. "
                         "This is the same analysis previously provided to and acknowledged by director. "
                         "Sharing workplace safety concerns with coworkers is protected activity.",
            "files": ["Oct_3_Whistleblowing_41percent_Screenshot 2025-10-14 at 8.56.10 AM.png",
                     "Oct_3_Whistleblowing_41percent_Screenshot 2025-10-07 at 4.06.43 PM.png"]
        },
        {
            "title": "OCTOBER 3, 2025 - CENSORSHIP DIRECTIVES",
            "description": "8:35 AM: 'Your messages are bordering on inappropriate'<br/>"
                         "8:50 AM: 'I am asking that you delete the post'<br/>"
                         "12:19 PM: 'This is a directive. Remove this message'<br/>"
                         "4:30 PM: Fourth deletion directive<br/>"
                         "Four censorship demands in 8 hours for sharing workplace safety concerns.",
            "files": ["Oct_3_Censorship_01_Screenshot 2025-10-07 at 4.07.16 PM.png",
                     "Oct_3_Censorship_02_Screenshot 2025-10-14 at 8.56.44 AM.png"]
        },
        {
            "title": "OCTOBER 8, 2025 - RETALIATORY DISCIPLINE",
            "description": "Final Written Warning issued - first disciplinary action in 9 months of employment. "
                         "Discipline occurs just 5 days after protected whistleblowing activity. "
                         "The timing and severity demonstrate clear retaliation.",
            "files": ["Oct_8_Final_Warning_Screenshot 2025-10-14 at 8.56.10 AM.png",
                     "Oct_8_Final_Warning_Screenshot 2025-10-07 at 4.06.55 PM.png"]
        }
    ]

    # Add each critical event
    for event in critical_events:
        story.append(Paragraph(event["title"], subtitle_style))
        story.append(Paragraph(event["description"], body_style))
        story.append(Spacer(1, 0.2*inch))

        # Add images if they exist
        for filename in event["files"]:
            img_path = evidence_dir / filename
            if img_path.exists():
                try:
                    # Resize image to fit page
                    img = RLImage(str(img_path), width=7*inch, height=4*inch, kind='proportional')
                    story.append(img)
                    story.append(Spacer(1, 0.2*inch))
                except:
                    story.append(Paragraph(f"[Evidence: {filename}]", body_style))
            else:
                # Check without prefix
                for f in evidence_dir.glob("*.png"):
                    if filename.split('_', 3)[-1] in f.name:
                        try:
                            img = RLImage(str(f), width=7*inch, height=4*inch, kind='proportional')
                            story.append(img)
                            story.append(Spacer(1, 0.2*inch))
                            break
                        except:
                            pass

        story.append(PageBreak())

    # Legal significance page
    story.append(Paragraph("LEGAL SIGNIFICANCE", subtitle_style))
    story.append(Paragraph(
        "This evidence demonstrates clear retaliation under Maryland whistleblower protection laws:",
        body_style))

    story.append(Paragraph(
        "<b>1. Protected Activity:</b> Reporting workplace safety concerns affecting patient care<br/>"
        "<b>2. Adverse Action:</b> Final Written Warning (severe discipline)<br/>"
        "<b>3. Causal Connection:</b> 5 days between whistleblowing and discipline<br/>"
        "<b>4. Pretext:</b> Same analysis praised by director, punished when shared with staff<br/>"
        "<b>5. Pattern:</b> Four censorship attempts before formal discipline",
        body_style))

    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(
        "<b>Maryland OSHA Filing Deadline:</b> November 7, 2025<br/>"
        "<b>Case Type:</b> Whistleblower Retaliation<br/>"
        "<b>Protected Activity:</b> Reporting workplace safety concerns",
        body_style))

    # Build PDF
    doc.build(story)

    print(f"\n✅ PDF Generated: {output_pdf}")
    print(f"   Size: {output_pdf.stat().st_size / 1024:.1f} KB")

    return str(output_pdf)

def create_evidence_summary():
    """Create JSON summary of all evidence"""
    import json

    evidence_dir = Path("/Users/ugochi141/Desktop/CRITICAL_EVIDENCE_QUICK")

    summary = {
        "case": "Whistleblower Retaliation - Largo Laboratory",
        "complainant": "Ugochi L. Ndubuisi",
        "deadline": "November 7, 2025",
        "critical_timeline": {
            "2025-07-14": {
                "event": "Investigation Ordered",
                "actor": "Director Nathaniel Burmeister",
                "significance": "Management directed investigation"
            },
            "2025-09-29": {
                "event": "Analysis Provided",
                "actor": "Ugochi L. Ndubuisi",
                "response": "Director acknowledged validity",
                "significance": "Concerns validated by management"
            },
            "2025-10-03_0821": {
                "event": "Whistleblowing",
                "content": "41.23% failure rate shared with staff",
                "significance": "Protected activity - workplace safety"
            },
            "2025-10-03_0835": {
                "event": "First Censorship Demand",
                "content": "Messages 'bordering on inappropriate'"
            },
            "2025-10-03_0850": {
                "event": "Second Censorship Demand",
                "content": "Delete the post"
            },
            "2025-10-03_1219": {
                "event": "Third Censorship Demand",
                "content": "This is a directive"
            },
            "2025-10-03_1630": {
                "event": "Fourth Censorship Demand",
                "content": "Final demand to remove"
            },
            "2025-10-08": {
                "event": "Final Written Warning",
                "significance": "First discipline in 9 months - clear retaliation"
            }
        },
        "files_organized": len(list(evidence_dir.glob("*.png"))),
        "generated": datetime.now().isoformat()
    }

    json_path = evidence_dir / "case_summary.json"
    with open(json_path, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"✅ Case Summary: {json_path}")

    return summary

if __name__ == "__main__":
    print("GENERATING LEGAL TIMELINE PDF")
    print("="*60)

    # Generate PDF
    pdf_path = create_legal_pdf()

    # Create summary
    summary = create_evidence_summary()

    print("\n" + "="*60)
    print("PROCESSING COMPLETE")
    print("="*60)
    print("\nCritical Documents Generated:")
    print(f"• Timeline PDF: {pdf_path}")
    print(f"• Evidence Folder: /Users/ugochi141/Desktop/CRITICAL_EVIDENCE_QUICK/")
    print(f"• Case Summary: case_summary.json")
    print("\n⚠️ Remember to file with Maryland OSHA by November 7, 2025")