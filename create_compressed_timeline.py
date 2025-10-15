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
import pytesseract
from dateutil import parser
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
import tempfile
import io

class CompressedTimelineCreator:
    def __init__(self):
        self.output_pdf = Path("/Users/ugochi141/Desktop/WHISTLEBLOWER_TIMELINE_COMPRESSED.pdf")
        self.temp_dir = Path(tempfile.mkdtemp())
        self.critical_evidence_dir = Path("/Users/ugochi141/Desktop/CRITICAL_EVIDENCE_QUICK")
        self.chronological_dir = Path("/Users/ugochi141/Desktop/LEGAL_TIMELINE/03_COMPLETE_CHRONOLOGICAL")
        self.largo_dir = Path("/Users/ugochi141/Desktop/Largo/Got me fucked up")

        # Critical dates to prioritize
        self.critical_dates = {
            "2025-07-14": "Investigation Ordered",
            "2025-07-15": "CA Path Directive",
            "2025-09-29": "Analysis Provided",
            "2025-10-03": "Whistleblowing & Censorship",
            "2025-10-08": "Final Written Warning"
        }

        self.critical_files = []
        self.max_size_mb = 48  # Leave buffer under 50MB

    def create_summary_pages(self):
        """Create summary pages as PDF"""
        summary_pdf = self.temp_dir / "00_summary.pdf"
        doc = SimpleDocTemplate(str(summary_pdf), pagesize=letter,
                              topMargin=0.75*inch, bottomMargin=0.75*inch,
                              leftMargin=0.75*inch, rightMargin=0.75*inch)

        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('Title',
                                    parent=styles['Heading1'],
                                    fontSize=22,
                                    textColor=HexColor('#000080'),
                                    spaceAfter=20,
                                    alignment=TA_CENTER)

        heading_style = ParagraphStyle('Heading',
                                      parent=styles['Heading2'],
                                      fontSize=16,
                                      textColor=HexColor('#800000'),
                                      spaceAfter=12,
                                      spaceBefore=12)

        body_style = styles['BodyText']
        body_style.fontSize = 11
        body_style.leading = 14

        story = []

        # Title Page
        story.append(Paragraph("WHISTLEBLOWER RETALIATION EVIDENCE", title_style))
        story.append(Paragraph("Largo Laboratory - Kaiser Permanente", heading_style))
        story.append(Spacer(1, 0.3*inch))

        # Executive Summary
        story.append(Paragraph("<b>EXECUTIVE SUMMARY</b>", heading_style))
        story.append(Paragraph(
            "This document presents chronological evidence of retaliation against Ugochi L. Ndubuisi "
            "for protected whistleblowing activity. The pattern shows: (1) Management ordered investigation, "
            "(2) Analysis was provided and acknowledged, (3) Same analysis shared with staff (protected activity), "
            "(4) Immediate censorship demands, (5) Final Written Warning within 5 days.", body_style))

        story.append(Spacer(1, 0.2*inch))

        # Timeline Table
        story.append(Paragraph("<b>CRITICAL TIMELINE</b>", heading_style))

        timeline_data = [
            ['Date', 'Event', 'Significance'],
            ['July 14, 2025', 'Investigation Ordered', 'Director orders investigation'],
            ['Sept 29, 2025', 'Analysis Provided', 'Comprehensive analysis acknowledged'],
            ['Oct 3, 2025 8:21am', 'Whistleblowing', '41.23% failure rate shared'],
            ['Oct 3, 2025 8:35am', '1st Censorship', '"Inappropriate" - 14 min after'],
            ['Oct 3, 2025 8:50am', '2nd Censorship', '"Delete post" - 29 min after'],
            ['Oct 3, 2025 12:19pm', '3rd Censorship', '"Directive" - escalation'],
            ['Oct 3, 2025 4:30pm', '4th Censorship', 'Final demand'],
            ['Oct 8, 2025', 'Final Warning', 'First discipline in 9 months']
        ]

        table = Table(timeline_data, colWidths=[1.5*inch, 2*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#000080')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, HexColor('#f0f0f0')])
        ]))

        story.append(table)
        story.append(PageBreak())

        # Pattern of Retaliation
        story.append(Paragraph("<b>PATTERN OF RETALIATION</b>", heading_style))

        pattern_points = [
            "<b>1. Protected Activity:</b> Reported workplace safety concerns (41.23% failure rate)",
            "<b>2. Temporal Proximity:</b> 5 days between whistleblowing and discipline",
            "<b>3. Disparate Treatment:</b> Same content praised by director, punished when shared",
            "<b>4. Censorship Pattern:</b> Four deletion demands in 8 hours",
            "<b>5. Clean Record:</b> First discipline in 9 months of employment",
            "<b>6. Severity:</b> Jumped directly to Final Written Warning"
        ]

        for point in pattern_points:
            story.append(Paragraph(point, body_style))
            story.append(Spacer(1, 0.1*inch))

        story.append(Spacer(1, 0.2*inch))

        # Filing Information
        story.append(Paragraph("<b>FILING INFORMATION</b>", heading_style))
        story.append(Paragraph(
            "<b>Maryland OSHA Deadline:</b> November 7, 2025<br/>"
            "<b>Case Type:</b> Whistleblower Retaliation<br/>"
            "<b>Protected Activity:</b> Reporting workplace safety concerns<br/>"
            "<b>Document Generated:</b> " + datetime.now().strftime("%B %d, %Y"),
            body_style))

        story.append(PageBreak())

        # Evidence Index
        story.append(Paragraph("<b>EVIDENCE INDEX</b>", heading_style))
        story.append(Paragraph("Critical documents included in this compressed filing:", body_style))
        story.append(Spacer(1, 0.1*inch))

        evidence_list = [
            "Page 3-4: July 14 - Investigation directive from Director",
            "Page 5-6: September 29 - Analysis provided and acknowledged",
            "Page 7-8: October 3 - Whistleblowing (41.23% shared)",
            "Page 9-12: October 3 - Four censorship demands",
            "Page 13-14: October 8 - Final Written Warning",
            "Supporting: Email chains, Teams messages, policy documents"
        ]

        for item in evidence_list:
            story.append(Paragraph("• " + item, body_style))

        # Build the summary PDF
        doc.build(story)

        return summary_pdf

    def compress_image(self, image_path, quality=30, max_size=(1200, 1200)):
        """Compress an image for smaller file size"""
        try:
            img = Image.open(image_path)

            # Convert RGBA to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = rgb_img

            # Resize if too large
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Save compressed
            output_path = self.temp_dir / f"compressed_{image_path.name}"
            img.save(output_path, 'JPEG', quality=quality, optimize=True)

            return output_path
        except Exception as e:
            print(f"Error compressing {image_path.name}: {e}")
            return None

    def convert_image_to_pdf(self, image_path, page_title=""):
        """Convert image to PDF with compression"""
        pdf_path = self.temp_dir / f"{image_path.stem}.pdf"

        c = canvas.Canvas(str(pdf_path), pagesize=letter)

        # Add title
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, 750, page_title)

        # Compress and add image
        compressed = self.compress_image(image_path)
        if compressed:
            try:
                c.drawImage(str(compressed), 50, 100, width=500, height=600, preserveAspectRatio=True)
            except:
                c.drawString(50, 400, f"[Image: {image_path.name}]")

        c.save()
        return pdf_path

    def select_critical_files(self):
        """Select only the most critical files to include"""
        print("\n1. SELECTING CRITICAL FILES")
        print("="*60)

        # Priority 1: Critical evidence from CRITICAL_EVIDENCE_QUICK
        critical_patterns = [
            "July_14_Investigation",
            "Sept_29_Analysis",
            "Oct_3_Whistleblowing",
            "Oct_3_Censorship",
            "Oct_8_Final_Warning"
        ]

        # Get critical screenshots
        for pattern in critical_patterns:
            for file in self.critical_evidence_dir.glob(f"*{pattern}*.png"):
                self.critical_files.append({
                    'path': file,
                    'priority': 1,
                    'type': 'critical_screenshot',
                    'date': self.extract_date_from_filename(file.name)
                })
                print(f"  ✓ Critical: {file.name}")

        # Priority 2: Key PDFs from Largo folder
        key_pdfs = ["Investigation.pdf", "Directive.pdf", "Analysis.pdf", "CA.pdf",
                   "Mail Corrospondence.pdf", "Evidence.docx"]

        for pdf_name in key_pdfs:
            pdf_path = self.largo_dir / pdf_name
            if pdf_path.exists():
                self.critical_files.append({
                    'path': pdf_path,
                    'priority': 2,
                    'type': 'pdf',
                    'date': None
                })
                print(f"  ✓ PDF: {pdf_name}")

        print(f"\nTotal critical files selected: {len(self.critical_files)}")

    def extract_date_from_filename(self, filename):
        """Extract date from filename if present"""
        match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
        if match:
            try:
                return datetime.strptime(match.group(1), '%Y-%m-%d')
            except:
                pass
        return None

    def create_compressed_timeline(self):
        """Create the compressed timeline PDF"""
        print("\n2. CREATING COMPRESSED PDF")
        print("="*60)

        merger = PdfMerger()

        # Add summary pages first
        print("Adding summary pages...")
        summary_pdf = self.create_summary_pages()
        merger.append(str(summary_pdf))

        # Sort files by priority and date
        self.critical_files.sort(key=lambda x: (x['priority'], x['date'] or datetime(2025, 1, 1)))

        # Process critical files
        for i, file_info in enumerate(self.critical_files):
            file_path = file_info['path']
            print(f"[{i+1}/{len(self.critical_files)}] Processing: {file_path.name}")

            try:
                if file_path.suffix == '.png':
                    # Convert compressed image to PDF
                    date_str = file_info['date'].strftime('%Y-%m-%d') if file_info['date'] else ""
                    pdf_path = self.convert_image_to_pdf(file_path, f"Evidence: {date_str} - {file_path.stem}")
                    if pdf_path and pdf_path.exists():
                        merger.append(str(pdf_path))

                elif file_path.suffix == '.pdf':
                    # Add first few pages of PDF only
                    reader = PdfReader(str(file_path))
                    writer = PdfWriter()

                    # Add only first 3 pages to keep size down
                    for page_num in range(min(3, len(reader.pages))):
                        writer.add_page(reader.pages[page_num])

                    temp_pdf = self.temp_dir / f"partial_{file_path.name}"
                    with open(temp_pdf, 'wb') as f:
                        writer.write(f)

                    merger.append(str(temp_pdf))

                # Check current size
                temp_output = self.temp_dir / "temp_merged.pdf"
                with open(temp_output, 'wb') as f:
                    merger.write(f)

                current_size_mb = temp_output.stat().st_size / (1024 * 1024)
                print(f"  Current size: {current_size_mb:.1f} MB")

                if current_size_mb > self.max_size_mb:
                    print(f"  ⚠ Approaching size limit, stopping at {i+1} files")
                    break

            except Exception as e:
                print(f"  Error processing {file_path.name}: {e}")

        # Write final PDF
        print(f"\nWriting final compressed PDF...")
        with open(self.output_pdf, 'wb') as output:
            merger.write(output)

        merger.close()

        final_size_mb = self.output_pdf.stat().st_size / (1024 * 1024)
        print(f"✓ Compressed PDF created: {final_size_mb:.1f} MB")

        return final_size_mb

    def verify_and_optimize(self):
        """Verify size and optimize if needed"""
        print("\n3. VERIFYING FILE SIZE")
        print("="*60)

        size_mb = self.output_pdf.stat().st_size / (1024 * 1024)

        if size_mb > 50:
            print(f"⚠ File too large ({size_mb:.1f} MB), applying additional compression...")

            # Apply additional compression using PyPDF2
            reader = PdfReader(str(self.output_pdf))
            writer = PdfWriter()

            for page in reader.pages:
                page.compress_content_streams()
                writer.add_page(page)

            optimized_path = self.output_pdf.parent / "WHISTLEBLOWER_TIMELINE_OPTIMIZED.pdf"
            with open(optimized_path, 'wb') as f:
                writer.write(f)

            # Replace with optimized version
            shutil.move(optimized_path, self.output_pdf)

            size_mb = self.output_pdf.stat().st_size / (1024 * 1024)

        print(f"✅ Final size: {size_mb:.1f} MB")

        if size_mb <= 50:
            print("✅ File is under 50MB limit - ready for upload!")
        else:
            print("⚠ File still exceeds 50MB - manual reduction may be needed")

        return size_mb

    def run(self):
        """Execute the compression process"""
        print("COMPRESSED TIMELINE CREATOR")
        print("Target: Under 50MB with integrated summary")
        print("="*60)

        # Select critical files only
        self.select_critical_files()

        # Create compressed timeline
        size_mb = self.create_compressed_timeline()

        # Verify and optimize if needed
        final_size = self.verify_and_optimize()

        print("\n" + "="*60)
        print("PROCESSING COMPLETE")
        print("="*60)
        print(f"\n✅ Compressed PDF: {self.output_pdf}")
        print(f"✅ Final size: {final_size:.1f} MB")
        print(f"✅ Status: {'Ready for upload' if final_size <= 50 else 'Needs further compression'}")
        print("\nThe compressed timeline includes:")
        print("  • Integrated summary and timeline")
        print("  • July 14 investigation directive")
        print("  • September 29 analysis")
        print("  • October 3 whistleblowing and censorship")
        print("  • October 8 Final Written Warning")
        print("  • Key supporting documents")

def main():
    creator = CompressedTimelineCreator()
    creator.run()

if __name__ == "__main__":
    main()