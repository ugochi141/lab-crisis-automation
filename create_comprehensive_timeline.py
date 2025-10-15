#!/usr/bin/env python3
"""
Comprehensive Timeline Creator for Whistleblower Retaliation Case
Merges all images, PDFs, and Word documents into chronological order
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
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from docx import Document
import tempfile

class ComprehensiveTimelineCreator:
    def __init__(self):
        self.chronological_dir = Path("/Users/ugochi141/Desktop/LEGAL_TIMELINE/03_COMPLETE_CHRONOLOGICAL")
        self.largo_dir = Path("/Users/ugochi141/Desktop/Largo/Got me fucked up")
        self.existing_pdf = Path("/Users/ugochi141/Desktop/WHISTLEBLOWER_TIMELINE_EVIDENCE.pdf")
        self.output_pdf = Path("/Users/ugochi141/Desktop/COMPREHENSIVE_WHISTLEBLOWER_TIMELINE.pdf")
        self.temp_dir = Path(tempfile.mkdtemp())
        self.timeline_items = []

    def extract_date_from_text(self, text):
        """Extract dates from text content"""
        if not text:
            return None

        # Patterns for different date formats
        patterns = [
            r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}',
            r'\d{1,2}/\d{1,2}/\d{4}',
            r'\d{1,2}/\d{1,2}/\d{2}',
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    # Handle 2-digit years
                    date_str = match.group(0)
                    if re.match(r'\d{1,2}/\d{1,2}/\d{2}$', date_str):
                        # Convert MM/DD/YY to MM/DD/20YY
                        parts = date_str.split('/')
                        if int(parts[2]) < 100:
                            parts[2] = '20' + parts[2]
                        date_str = '/'.join(parts)

                    parsed_date = parser.parse(date_str, fuzzy=False)
                    # Only accept dates from 2025
                    if parsed_date.year == 2025:
                        return parsed_date
                except:
                    continue

        return None

    def identify_event_type(self, text):
        """Identify the type of event based on content"""
        text_lower = text.lower() if text else ""

        if "final written warning" in text_lower or "corrective action" in text_lower:
            return "FINAL_WARNING"
        elif "41.23" in text_lower or "failure rate" in text_lower:
            return "WHISTLEBLOWING"
        elif "delete" in text_lower and ("directive" in text_lower or "inappropriate" in text_lower):
            return "CENSORSHIP"
        elif "investigate" in text_lower and "second shift" in text_lower:
            return "INVESTIGATION"
        elif "culture issue" in text_lower or "runs deeper" in text_lower:
            return "ANALYSIS"
        elif "nathaniel" in text_lower:
            return "DIRECTIVE"
        elif "ugochi" in text_lower:
            return "RESPONSE"
        else:
            return "DOCUMENT"

    def process_image_file(self, image_path):
        """Process a single image file and extract date/content"""
        print(f"  Processing image: {image_path.name}")

        try:
            # Quick OCR
            img = Image.open(image_path)
            img.thumbnail((1500, 1500), Image.Resampling.LANCZOS)
            text = pytesseract.image_to_string(img)

            # Extract date
            date = self.extract_date_from_text(text)

            # Identify event type
            event_type = self.identify_event_type(text)

            # Create timeline item
            item = {
                'date': date,
                'type': 'image',
                'event_type': event_type,
                'path': image_path,
                'text_preview': text[:200] if text else "",
                'source': 'LEGAL_TIMELINE'
            }

            return item

        except Exception as e:
            print(f"    Error processing {image_path.name}: {e}")
            return None

    def process_pdf_file(self, pdf_path):
        """Process a PDF file and extract date/content"""
        print(f"  Processing PDF: {pdf_path.name}")

        try:
            reader = PdfReader(pdf_path)
            text = ""

            # Extract text from first few pages
            for i, page in enumerate(reader.pages[:3]):
                text += page.extract_text()
                if len(text) > 1000:
                    break

            # Extract date
            date = self.extract_date_from_text(text)

            # Identify event type
            event_type = self.identify_event_type(text)

            # Create timeline item
            item = {
                'date': date,
                'type': 'pdf',
                'event_type': event_type,
                'path': pdf_path,
                'text_preview': text[:200] if text else "",
                'source': 'Largo',
                'pages': len(reader.pages)
            }

            return item

        except Exception as e:
            print(f"    Error processing {pdf_path.name}: {e}")
            return None

    def process_word_file(self, docx_path):
        """Process a Word document and extract date/content"""
        print(f"  Processing Word doc: {docx_path.name}")

        try:
            doc = Document(docx_path)
            text = "\n".join([p.text for p in doc.paragraphs[:20]])

            # Extract date
            date = self.extract_date_from_text(text)

            # Identify event type
            event_type = self.identify_event_type(text)

            # Convert to PDF for inclusion
            temp_pdf = self.temp_dir / f"{docx_path.stem}.pdf"

            # Create timeline item
            item = {
                'date': date,
                'type': 'docx',
                'event_type': event_type,
                'path': docx_path,
                'text_preview': text[:200] if text else "",
                'source': 'Largo'
            }

            return item

        except Exception as e:
            print(f"    Error processing {docx_path.name}: {e}")
            return None

    def collect_all_files(self):
        """Collect and process all files from both locations"""
        print("\n1. COLLECTING FILES")
        print("="*60)

        # Process images from LEGAL_TIMELINE
        print("\nProcessing LEGAL_TIMELINE images...")
        for img_path in self.chronological_dir.glob("*.png"):
            item = self.process_image_file(img_path)
            if item:
                self.timeline_items.append(item)

        # Process PDFs from Largo folder
        print("\nProcessing Largo PDFs...")
        for pdf_path in self.largo_dir.rglob("*.pdf"):
            # Skip the Gmail PDFs as they're likely duplicates
            if "Gmail" not in pdf_path.name and "Outlook" not in pdf_path.name:
                item = self.process_pdf_file(pdf_path)
                if item:
                    self.timeline_items.append(item)

        # Process Word docs from Largo folder
        print("\nProcessing Largo Word documents...")
        for docx_path in self.largo_dir.glob("*.docx"):
            item = self.process_word_file(docx_path)
            if item:
                self.timeline_items.append(item)

        print(f"\nTotal items collected: {len(self.timeline_items)}")

    def sort_timeline(self):
        """Sort all items by date, with undated items at the end"""
        print("\n2. SORTING TIMELINE")
        print("="*60)

        # Separate dated and undated items
        dated_items = [item for item in self.timeline_items if item['date']]
        undated_items = [item for item in self.timeline_items if not item['date']]

        # Sort dated items
        dated_items.sort(key=lambda x: x['date'])

        # Sort undated items by event type priority
        priority_order = {
            'INVESTIGATION': 1,
            'ANALYSIS': 2,
            'WHISTLEBLOWING': 3,
            'CENSORSHIP': 4,
            'FINAL_WARNING': 5,
            'DIRECTIVE': 6,
            'RESPONSE': 7,
            'DOCUMENT': 8
        }

        undated_items.sort(key=lambda x: priority_order.get(x['event_type'], 9))

        # Combine
        self.timeline_items = dated_items + undated_items

        # Print summary
        print(f"Dated items: {len(dated_items)}")
        print(f"Undated items: {len(undated_items)}")

        # Show date distribution
        if dated_items:
            print("\nDate distribution:")
            date_counts = {}
            for item in dated_items:
                month_key = item['date'].strftime('%Y-%m')
                date_counts[month_key] = date_counts.get(month_key, 0) + 1

            for month, count in sorted(date_counts.items()):
                print(f"  {month}: {count} items")

    def create_comprehensive_pdf(self):
        """Create the comprehensive timeline PDF"""
        print("\n3. CREATING COMPREHENSIVE PDF")
        print("="*60)

        merger = PdfMerger()

        # Add existing timeline PDF first if it exists
        if self.existing_pdf.exists():
            print("Adding existing timeline PDF...")
            merger.append(str(self.existing_pdf))

        # Process each timeline item
        for i, item in enumerate(self.timeline_items):
            date_str = item['date'].strftime('%Y-%m-%d') if item['date'] else "Undated"
            print(f"[{i+1}/{len(self.timeline_items)}] Adding: {date_str} - {item['event_type']} - {item['path'].name}")

            try:
                if item['type'] == 'image':
                    # Convert image to PDF
                    temp_pdf = self.temp_dir / f"img_{i:04d}.pdf"
                    self.image_to_pdf(item['path'], temp_pdf, date_str, item['event_type'])
                    merger.append(str(temp_pdf))

                elif item['type'] == 'pdf':
                    # Add PDF directly
                    merger.append(str(item['path']))

                elif item['type'] == 'docx':
                    # Skip Word docs for now (would need python-docx2pdf)
                    print(f"  Note: Word doc {item['path'].name} - manual conversion needed")

            except Exception as e:
                print(f"  Error adding {item['path'].name}: {e}")

        # Write the merged PDF
        print(f"\nWriting comprehensive PDF to: {self.output_pdf}")
        with open(self.output_pdf, 'wb') as output:
            merger.write(output)

        merger.close()

        print(f"✓ PDF created successfully!")
        print(f"  Size: {self.output_pdf.stat().st_size / (1024*1024):.2f} MB")

    def image_to_pdf(self, image_path, pdf_path, date_str, event_type):
        """Convert an image to PDF with header"""
        c = canvas.Canvas(str(pdf_path), pagesize=letter)

        # Add header
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 750, f"Date: {date_str}")
        c.drawString(50, 735, f"Type: {event_type}")
        c.drawString(50, 720, f"Source: {image_path.name}")

        # Add image
        try:
            img = Image.open(image_path)

            # Calculate scaling to fit on page
            max_width = 500
            max_height = 650

            img_width, img_height = img.size
            scale = min(max_width/img_width, max_height/img_height, 1.0)

            new_width = int(img_width * scale)
            new_height = int(img_height * scale)

            # Center the image
            x = (letter[0] - new_width) / 2
            y = 50

            c.drawImage(str(image_path), x, y, width=new_width, height=new_height)

        except Exception as e:
            c.drawString(50, 400, f"Error loading image: {e}")

        c.save()

    def generate_summary_report(self):
        """Generate a summary report of the timeline"""
        print("\n4. GENERATING SUMMARY REPORT")
        print("="*60)

        report_path = self.output_pdf.parent / "TIMELINE_SUMMARY_REPORT.txt"

        with open(report_path, 'w') as f:
            f.write("COMPREHENSIVE TIMELINE SUMMARY REPORT\n")
            f.write("="*60 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total items: {len(self.timeline_items)}\n\n")

            f.write("CHRONOLOGICAL EVENTS:\n")
            f.write("-"*40 + "\n\n")

            for item in self.timeline_items:
                date_str = item['date'].strftime('%Y-%m-%d') if item['date'] else "Undated"
                f.write(f"{date_str} | {item['event_type']:<15} | {item['path'].name}\n")
                if item['text_preview']:
                    f.write(f"  Preview: {item['text_preview'][:100]}...\n")
                f.write("\n")

            # Event type summary
            f.write("\nEVENT TYPE SUMMARY:\n")
            f.write("-"*40 + "\n")
            event_counts = {}
            for item in self.timeline_items:
                event_counts[item['event_type']] = event_counts.get(item['event_type'], 0) + 1

            for event_type, count in sorted(event_counts.items()):
                f.write(f"{event_type:<20}: {count} items\n")

        print(f"✓ Summary report saved to: {report_path}")

    def run(self):
        """Execute the complete timeline creation process"""
        print("COMPREHENSIVE TIMELINE CREATOR")
        print("Whistleblower Retaliation Case")
        print("="*60)

        # Collect all files
        self.collect_all_files()

        # Sort by date
        self.sort_timeline()

        # Create comprehensive PDF
        self.create_comprehensive_pdf()

        # Generate summary report
        self.generate_summary_report()

        print("\n" + "="*60)
        print("PROCESSING COMPLETE")
        print("="*60)
        print(f"\n✅ Comprehensive PDF: {self.output_pdf}")
        print(f"✅ Items processed: {len(self.timeline_items)}")
        print("\nThe comprehensive timeline includes:")
        print("  • All images from LEGAL_TIMELINE folder")
        print("  • All PDFs from Largo folder")
        print("  • Existing timeline PDF merged at beginning")
        print("  • Everything sorted chronologically by actual dates")

def main():
    creator = ComprehensiveTimelineCreator()
    creator.run()

if __name__ == "__main__":
    main()