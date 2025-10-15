#!/usr/bin/env python3
"""
Create Compressed Timeline PDF (Under 50MB) with Integrated Summary
Whistleblower Retaliation Case - Maryland OSHA Filing
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas
import tempfile

class CompressedTimelineCreator:
    def __init__(self):
        self.output_pdf = Path("/Users/ugochi141/Desktop/WHISTLEBLOWER_TIMELINE_COMPRESSED.pdf")
        self.temp_dir = Path(tempfile.mkdtemp())
        self.critical_evidence_dir = Path("/Users/ugochi141/Desktop/CRITICAL_EVIDENCE_QUICK")
        self.largo_dir = Path("/Users/ugochi141/Desktop/Largo/Got me fucked up")
        self.critical_files = []
        self.max_size_mb = 45  # Target size with buffer

    def create_summary_pages(self):
        """Create summary pages as PDF"""
        summary_pdf = self.temp_dir / "00_summary.pdf"
        doc = SimpleDocTemplate(str(summary_pdf), pagesize=letter,
                              topMargin=0.5*inch, bottomMargin=0.5*inch,
                              leftMargin=0.5*inch, rightMargin=0.5*inch)

        styles = getSampleStyleSheet()
        story = []

        # Title Page
        title_style = styles['Title']
        title_style.fontSize = 20
        title_style.alignment = TA_CENTER

        story.append(Paragraph("WHISTLEBLOWER RETALIATION EVIDENCE", title_style))
        story.append(Paragraph("Largo Laboratory - Kaiser Permanente", styles['Heading2']))
        story.append(Spacer(1, 0.5*inch))

        # Executive Summary
        story.append(Paragraph("<b>EXECUTIVE SUMMARY</b>", styles['Heading2']))
        summary_text = """This document presents chronological evidence of retaliation against
        Ugochi L. Ndubuisi for protected whistleblowing activity. The timeline shows:
        <br/><br/>
        1. July 14, 2025: Director orders investigation<br/>
        2. September 29, 2025: Analysis provided and acknowledged<br/>
        3. October 3, 2025: Same analysis shared with staff (protected activity)<br/>
        4. October 3, 2025: Four censorship demands in 8 hours<br/>
        5. October 8, 2025: Final Written Warning (first discipline in 9 months)<br/>
        <br/>
        <b>Maryland OSHA Deadline: November 7, 2025</b>
        """
        story.append(Paragraph(summary_text, styles['BodyText']))
        story.append(PageBreak())

        # Critical Timeline Table
        story.append(Paragraph("<b>CRITICAL TIMELINE</b>", styles['Heading2']))

        timeline_data = [
            ['Date/Time', 'Event', 'Significance'],
            ['July 14, 2025', 'Investigation Ordered', 'Director orders investigation into second shift'],
            ['Sept 29, 2025', 'Analysis Provided', '"Culture issue runs deeper" - acknowledged by director'],
            ['Oct 3, 8:21am', 'Whistleblowing', '41.23% failure rate shared with staff'],
            ['Oct 3, 8:35am', 'Censorship #1', '"Inappropriate" - 14 minutes after sharing'],
            ['Oct 3, 8:50am', 'Censorship #2', '"Delete the post" - 29 minutes after'],
            ['Oct 3, 12:19pm', 'Censorship #3', '"This is a directive" - escalation'],
            ['Oct 3, 4:30pm', 'Censorship #4', 'Fourth deletion demand'],
            ['Oct 8, 2025', 'Final Warning', 'First discipline ever - clear retaliation']
        ]

        table = Table(timeline_data, colWidths=[1.3*inch, 1.8*inch, 3.4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))

        story.append(table)
        story.append(PageBreak())

        # Pattern of Retaliation
        story.append(Paragraph("<b>PATTERN OF RETALIATION - KEY EVIDENCE</b>", styles['Heading2']))

        pattern_text = """
        <b>1. Protected Activity:</b> Reported workplace safety concerns affecting patient care (41.23% failure rate)
        <br/><br/>
        <b>2. Temporal Proximity:</b> Only 5 days between whistleblowing and Final Written Warning
        <br/><br/>
        <b>3. Disparate Treatment:</b> Same analysis praised by director on Sept 29, punished when shared Oct 3
        <br/><br/>
        <b>4. Censorship Pattern:</b> Four deletion demands in single day shows intent to silence
        <br/><br/>
        <b>5. Clean Employment Record:</b> No prior discipline in 9 months - sudden jump to Final Warning
        <br/><br/>
        <b>6. Public Interest:</b> Patient safety at Level 3 Trauma facility serving community
        <br/><br/>
        <b>Filing Information:</b><br/>
        • Maryland OSHA Deadline: November 7, 2025<br/>
        • Protected under Maryland Occupational Safety and Health Act<br/>
        • Document Generated: """ + datetime.now().strftime("%B %d, %Y")

        story.append(Paragraph(pattern_text, styles['BodyText']))

        # Build PDF
        doc.build(story)
        return summary_pdf

    def compress_image_to_pdf(self, image_path, title="", max_width=1000):
        """Convert and compress image to PDF"""
        pdf_path = self.temp_dir / f"{image_path.stem}_compressed.pdf"

        try:
            # Open and compress image
            img = Image.open(image_path)

            # Convert to RGB if needed
            if img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    rgb_img.paste(img, mask=img.split()[-1])
                else:
                    rgb_img.paste(img)
                img = rgb_img

            # Resize if too large
            if img.width > max_width:
                ratio = max_width / img.width
                new_size = (max_width, int(img.height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)

            # Save as compressed JPEG first
            temp_jpg = self.temp_dir / f"{image_path.stem}.jpg"
            img.save(temp_jpg, 'JPEG', quality=40, optimize=True)

            # Create PDF with the compressed image
            c = canvas.Canvas(str(pdf_path), pagesize=letter)

            # Add title
            c.setFont("Helvetica-Bold", 10)
            c.drawString(30, 750, title[:80] if title else image_path.name[:80])

            # Add compressed image
            img_width = min(img.width, 550)
            img_height = min(img.height, 700)

            c.drawImage(str(temp_jpg), 30, 40, width=img_width, height=img_height,
                       preserveAspectRatio=True, mask='auto')

            c.save()

            # Clean up temp file
            temp_jpg.unlink(missing_ok=True)

            return pdf_path

        except Exception as e:
            print(f"  Error compressing {image_path.name}: {e}")
            return None

    def select_critical_files(self):
        """Select only the most critical evidence files"""
        print("\n1. SELECTING CRITICAL EVIDENCE")
        print("="*60)

        # Priority 1: Critical screenshots from CRITICAL_EVIDENCE_QUICK
        if self.critical_evidence_dir.exists():
            critical_patterns = [
                "*July_14_Investigation*.png",
                "*Sept_29_Analysis*.png",
                "*Oct_3_Whistleblowing*.png",
                "*Oct_3_Censorship*.png",
                "*Oct_8_Final_Warning*.png"
            ]

            for pattern in critical_patterns:
                for file in self.critical_evidence_dir.glob(pattern):
                    self.critical_files.append({
                        'path': file,
                        'priority': 1,
                        'type': 'image'
                    })
                    print(f"  ✓ Critical: {file.name}")

        # Priority 2: Key PDFs (only most essential)
        essential_pdfs = [
            "CA.pdf",  # Final Warning
            "Investigation.pdf",
            "Directive.pdf",
            "Analysis.pdf"
        ]

        for pdf_name in essential_pdfs:
            pdf_path = self.largo_dir / pdf_name
            if pdf_path.exists():
                self.critical_files.append({
                    'path': pdf_path,
                    'priority': 2,
                    'type': 'pdf'
                })
                print(f"  ✓ PDF: {pdf_name}")

        print(f"\nTotal critical files: {len(self.critical_files)}")

    def create_compressed_pdf(self):
        """Create the final compressed PDF"""
        print("\n2. CREATING COMPRESSED PDF")
        print("="*60)

        merger = PdfMerger()
        current_size = 0

        # Add summary first
        print("Adding summary pages...")
        summary_pdf = self.create_summary_pages()
        merger.append(str(summary_pdf))

        # Sort files by priority
        self.critical_files.sort(key=lambda x: x['priority'])

        # Process each critical file
        for i, file_info in enumerate(self.critical_files, 1):
            file_path = file_info['path']
            print(f"[{i}/{len(self.critical_files)}] Processing: {file_path.name[:40]}")

            try:
                if file_info['type'] == 'image':
                    # Compress and convert image
                    pdf_path = self.compress_image_to_pdf(
                        file_path,
                        f"Evidence {i}: {file_path.stem}"
                    )
                    if pdf_path and pdf_path.exists():
                        merger.append(str(pdf_path))
                        current_size = self.check_size(merger)

                elif file_info['type'] == 'pdf':
                    # Add only first 2 pages of PDFs
                    reader = PdfReader(str(file_path))
                    writer = PdfWriter()

                    pages_to_add = min(2, len(reader.pages))
                    for page_num in range(pages_to_add):
                        page = reader.pages[page_num]
                        page.compress_content_streams()
                        writer.add_page(page)

                    temp_pdf = self.temp_dir / f"partial_{file_path.name}"
                    with open(temp_pdf, 'wb') as f:
                        writer.write(f)

                    merger.append(str(temp_pdf))
                    current_size = self.check_size(merger)

                # Stop if getting too large
                if current_size > self.max_size_mb:
                    print(f"  ⚠ Approaching size limit ({current_size:.1f} MB), stopping here")
                    break

            except Exception as e:
                print(f"  Error: {e}")
                continue

        # Write final PDF
        print("\nWriting final PDF...")
        with open(self.output_pdf, 'wb') as output:
            merger.write(output)

        merger.close()

        final_size = self.output_pdf.stat().st_size / (1024 * 1024)
        print(f"✓ PDF created: {final_size:.1f} MB")

        return final_size

    def check_size(self, merger):
        """Check current size of merged PDF"""
        temp_file = self.temp_dir / "temp_check.pdf"
        with open(temp_file, 'wb') as f:
            merger.write(f)
        size_mb = temp_file.stat().st_size / (1024 * 1024)
        return size_mb

    def run(self):
        """Main execution"""
        print("COMPRESSED TIMELINE CREATOR")
        print("Creating PDF under 50MB with integrated summary")
        print("="*60)

        # Select critical files
        self.select_critical_files()

        # Create compressed PDF
        final_size = self.create_compressed_pdf()

        # Clean up temp directory
        shutil.rmtree(self.temp_dir, ignore_errors=True)

        print("\n" + "="*60)
        print("PROCESSING COMPLETE")
        print("="*60)
        print(f"\n✅ Output: {self.output_pdf}")
        print(f"✅ Size: {final_size:.1f} MB")
        print(f"✅ Status: {'READY FOR UPLOAD' if final_size < 50 else 'NEEDS FURTHER COMPRESSION'}")
        print("\nIncludes:")
        print("  • Integrated executive summary and timeline table")
        print("  • July 14 investigation directive")
        print("  • September 29 analysis and acknowledgment")
        print("  • October 3 whistleblowing and censorship")
        print("  • October 8 Final Written Warning")
        print("  • All compressed to stay under 50MB")

def main():
    creator = CompressedTimelineCreator()
    creator.run()

if __name__ == "__main__":
    main()