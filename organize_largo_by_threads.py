#!/usr/bin/env python3
"""
Reorganize Largo documents by conversation threads and topics.
Groups related screenshots together as complete conversations.
"""

import os
import glob
from datetime import datetime
from pathlib import Path
import subprocess
import tempfile
import shutil
from PIL import Image
from pypdf import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor


def create_section_divider(title, subtitle=""):
    """Create a PDF page as a section divider."""
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    c = canvas.Canvas(temp_pdf.name, pagesize=letter)

    # Background
    c.setFillColor(HexColor('#1e3a8a'))  # Dark blue
    c.rect(0, 0, 612, 792, fill=True, stroke=False)

    # Title
    c.setFillColor(HexColor('#ffffff'))
    c.setFont("Helvetica-Bold", 28)

    # Handle long titles
    if len(title) > 50:
        words = title.split()
        line1 = ' '.join(words[:len(words)//2])
        line2 = ' '.join(words[len(words)//2:])
        c.drawCentredString(306, 520, line1)
        c.drawCentredString(306, 480, line2)
    else:
        c.drawCentredString(306, 500, title)

    # Subtitle
    if subtitle:
        c.setFont("Helvetica", 16)
        c.drawCentredString(306, 440, subtitle)

    c.save()
    return temp_pdf.name


def create_subsection_divider(title, subtitle=""):
    """Create a PDF page as a subsection divider."""
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    c = canvas.Canvas(temp_pdf.name, pagesize=letter)

    # Background
    c.setFillColor(HexColor('#3b82f6'))  # Lighter blue
    c.rect(0, 0, 612, 792, fill=True, stroke=False)

    # Title
    c.setFillColor(HexColor('#ffffff'))
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(306, 500, title)

    # Subtitle
    if subtitle:
        c.setFont("Helvetica", 14)
        c.drawCentredString(306, 460, subtitle)

    c.save()
    return temp_pdf.name


def create_table_of_contents(categories):
    """Create a table of contents page."""
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    c = canvas.Canvas(temp_pdf.name, pagesize=letter)

    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(306, 700, "Largo Laboratory Documentation")

    c.setFont("Helvetica", 14)
    c.drawCentredString(306, 670, "Organized by Topic & Conversation Thread")
    c.drawCentredString(306, 650, f"Generated: {datetime.now().strftime('%B %d, %Y')}")

    # Table of Contents
    c.setFont("Helvetica-Bold", 18)
    c.drawString(72, 600, "Table of Contents")

    y = 560
    c.setFont("Helvetica", 11)

    for idx, (category_name, items) in enumerate(categories.items(), 1):
        if y < 100:  # New page if needed
            c.showPage()
            y = 700

        c.setFont("Helvetica-Bold", 11)
        c.drawString(72, y, f"{idx}. {category_name}")
        y -= 15

        # Count total files
        if isinstance(items, dict):
            total_files = sum(len(files) for files in items.values())
        else:
            total_files = len(items)

        c.setFont("Helvetica", 9)
        c.drawString(90, y, f"({total_files} documents)")
        y -= 20

    c.save()
    return temp_pdf.name


def convert_image_to_pdf(image_path, output_pdf):
    """Convert an image to PDF."""
    try:
        img = Image.open(image_path)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        img.save(output_pdf, 'PDF', resolution=100.0)
        return True
    except Exception as e:
        print(f"Error converting image {image_path}: {e}")
        return False


def convert_docx_to_pdf_mac(docx_path, output_pdf):
    """Convert DOCX to PDF on macOS using LibreOffice."""
    try:
        result = subprocess.run(['which', 'soffice'], capture_output=True, text=True)

        if result.returncode == 0:
            temp_dir = tempfile.mkdtemp()
            subprocess.run([
                'soffice', '--headless', '--convert-to', 'pdf',
                '--outdir', temp_dir, docx_path
            ], check=True, capture_output=True)

            pdf_name = os.path.splitext(os.path.basename(docx_path))[0] + '.pdf'
            generated_pdf = os.path.join(temp_dir, pdf_name)

            if os.path.exists(generated_pdf):
                shutil.move(generated_pdf, output_pdf)
                shutil.rmtree(temp_dir, ignore_errors=True)
                return True
            else:
                shutil.rmtree(temp_dir, ignore_errors=True)
                return False
        else:
            # Create placeholder
            c = canvas.Canvas(output_pdf, pagesize=letter)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(100, 750, "DOCX Document (Conversion Not Available)")
            c.setFont("Helvetica", 12)
            c.drawString(100, 720, f"Filename: {os.path.basename(docx_path)}")
            c.save()
            return True
    except Exception as e:
        print(f"Error converting DOCX {docx_path}: {e}")
        return False


def categorize_files_by_threads(source_dir):
    """Categorize files and group related screenshots as conversation threads."""

    categories = {
        "1. Leave/PTO Disputes": {},
        "2. Manager Communications - Conversation Threads": {},
        "3. Staffing & Performance Issues": [],
        "4. Blood Bank Training & Investigations": [],
        "5. Team Chat Concerns - Early Conversations": [],
        "6. Policy & HR Documents": [],
        "7. Performance Analysis & Planning": [],
        "8. Other Documentation": []
    }

    # Get all files
    file_patterns = ['*.pdf', '*.png', '*.jpg', '*.jpeg', '*.docx']
    all_files = []

    for pattern in file_patterns:
        all_files.extend(glob.glob(os.path.join(source_dir, pattern)))
        all_files.extend(glob.glob(os.path.join(source_dir, '**', pattern), recursive=True))

    all_files = list(set(all_files))
    all_files.sort(key=lambda x: os.path.getmtime(x))

    # Define conversation threads (grouped screenshots)
    conversation_threads = {
        "Thread 1: July Performance Discussions": [],
        "Thread 2: September Re-integration Planning": [],
        "Thread 3: September Performance & Culture": [],
        "Thread 4: October - Team Chat & Inappropriate Messages": [],
        "Thread 5: October 14 - Performance, Accountability & Workplace Culture": [],
        "Thread 6: Other Manager Communications": []
    }

    # PTO related threads
    pto_threads = {
        "PTO Discussion Screenshots": [],
        "PTO Rejection Emails": []
    }

    # Early team chat threads (Oct 3 evening)
    team_chat_early = []

    for file_path in all_files:
        filename = os.path.basename(file_path).lower()
        file_date = datetime.fromtimestamp(os.path.getmtime(file_path))
        categorized = False

        # Policy documents
        if any(keyword in filename for keyword in ['policy', 'eeoc', 'at will', 'corrective', 'hr', 'cp_576', 'compliant']):
            if 'training' not in filename:  # Training might be different context
                categories["6. Policy & HR Documents"].append(file_path)
                categorized = True

        # Performance/Analysis
        elif any(keyword in filename for keyword in ['performance', 'analysis', 'improvement plan']):
            categories["7. Performance Analysis & Planning"].append(file_path)
            categorized = True

        # Blood bank, training, investigation
        elif any(keyword in filename for keyword in ['investigation', 'toe', 'directive', 'training']):
            categories["4. Blood Bank Training & Investigations"].append(file_path)
            categorized = True

        # Lab delays, staffing
        elif any(keyword in filename for keyword in ['delay', 'staffing', 'wlu', 'credential', 'phleb']):
            categories["3. Staffing & Performance Issues"].append(file_path)
            categorized = True

        # PTO/Leave emails
        elif any(keyword in filename for keyword in ['rejection', 'rejected', 'absence']):
            pto_threads["PTO Rejection Emails"].append(file_path)
            categorized = True

        # Screenshots - group by time/context
        elif 'screenshot' in filename:
            # Oct 3 evening (8:35 PM - 8:43 PM) - Early team chat concerns
            if '2025-10-03' in filename and ('8.3' in filename or '8.4' in filename):
                team_chat_early.append(file_path)
                categorized = True

            # Oct 13-14 PTO related screenshots
            elif any(time in filename for time in ['12.06.59', '5.59.48', '6.00.11', '6.00.35', '12.06.14']):
                pto_threads["PTO Discussion Screenshots"].append(file_path)
                categorized = True

            # Oct 14 8:56 AM thread - Performance & Culture conversation
            elif '2025-10-14' in filename and '8.56' in filename:
                conversation_threads["Thread 5: October 14 - Performance, Accountability & Workplace Culture"].append(file_path)
                categorized = True

            # Oct 14 8:40-8:55 AM - Manager communications
            elif '2025-10-14' in filename and any(time in filename for time in ['8.40', '8.46', '8.51', '8.53', '8.54', '8.55']):
                conversation_threads["Thread 4: October - Team Chat & Inappropriate Messages"].append(file_path)
                categorized = True

            # Oct 7 4:05-4:07 PM - Long conversation thread
            elif '2025-10-07' in filename and ('4.0' in filename or '3.57' in filename):
                conversation_threads["Thread 2: September Re-integration Planning"].append(file_path)
                categorized = True

            # Oct 7 morning (9:03-9:06 AM)
            elif '2025-10-07' in filename and '9.0' in filename:
                conversation_threads["Thread 1: July Performance Discussions"].append(file_path)
                categorized = True

            # Other October screenshots
            elif '2025-10' in filename:
                conversation_threads["Thread 6: Other Manager Communications"].append(file_path)
                categorized = True

        # Communication/correspondence PDFs
        elif any(keyword in filename for keyword in ['mail', 'outlook', 'correspondence', 'exchange', 'urgent']):
            conversation_threads["Thread 6: Other Manager Communications"].append(file_path)
            categorized = True

        # Other documents
        if not categorized:
            if filename.endswith('.docx'):
                categories["8. Other Documentation"].append(file_path)
            elif not any(file_path in v for cat in categories.values() for v in (cat.values() if isinstance(cat, dict) else [cat])):
                categories["8. Other Documentation"].append(file_path)

    # Assign threads to categories
    categories["1. Leave/PTO Disputes"] = pto_threads
    categories["2. Manager Communications - Conversation Threads"] = conversation_threads
    categories["5. Team Chat Concerns - Early Conversations"] = team_chat_early

    # Remove empty categories
    categories = {k: v for k, v in categories.items() if v}

    return categories


def merge_pdfs_by_threads(source_dir, output_path):
    """Main function to merge documents organized by threads."""

    print("=" * 80)
    print("Largo Documents - Organized by Conversation Threads")
    print("=" * 80)
    print(f"\nScanning: {source_dir}\n")

    categories = categorize_files_by_threads(source_dir)

    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    writer = PdfWriter()

    try:
        # Add table of contents
        print("Creating Table of Contents...")
        toc_pdf = create_table_of_contents(categories)
        reader = PdfReader(toc_pdf)
        for page in reader.pages:
            writer.add_page(page)
        os.unlink(toc_pdf)

        # Process each category
        for category_name, items in categories.items():
            print(f"\n{'='*80}")
            print(f"{category_name}")
            print('='*80)

            # Add main section divider
            if isinstance(items, dict):
                total_files = sum(len(files) for files in items.values())
            else:
                total_files = len(items)

            divider_pdf = create_section_divider(category_name, f"{total_files} documents")
            reader = PdfReader(divider_pdf)
            for page in reader.pages:
                writer.add_page(page)
            os.unlink(divider_pdf)

            # Handle nested threads
            if isinstance(items, dict):
                for thread_name, files in items.items():
                    if not files:
                        continue

                    print(f"\n  {thread_name} ({len(files)} files)")
                    print(f"  {'-'*76}")

                    # Add subsection divider
                    subdiv_pdf = create_subsection_divider(thread_name, f"{len(files)} documents")
                    reader = PdfReader(subdiv_pdf)
                    for page in reader.pages:
                        writer.add_page(page)
                    os.unlink(subdiv_pdf)

                    # Process files
                    process_files(files, writer, temp_dir)

            else:
                # Simple list of files
                process_files(items, writer, temp_dir)

        # Write final PDF
        print("\n" + "=" * 80)
        print("Writing final PDF...")

        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        print(f"\nSuccess! Created: {output_path}")
        print(f"Total pages: {len(writer.pages)}")

        file_size = os.path.getsize(output_path)
        file_size_mb = file_size / (1024 * 1024)
        print(f"File size: {file_size_mb:.2f} MB")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    print("=" * 80)


def process_files(files, writer, temp_dir):
    """Process and add files to the PDF writer."""
    for idx, file_path in enumerate(sorted(files, key=lambda x: os.path.getmtime(x)), 1):
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_path)[1].lower()
        timestamp = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')

        print(f"    {idx:2d}. [{timestamp}] {file_name}")

        temp_pdf = os.path.join(temp_dir, f"{idx:03d}_{file_name}.pdf")

        try:
            if file_ext == '.pdf':
                shutil.copy2(file_path, temp_pdf)
            elif file_ext in ['.png', '.jpg', '.jpeg']:
                if not convert_image_to_pdf(file_path, temp_pdf):
                    continue
            elif file_ext == '.docx':
                if not convert_docx_to_pdf_mac(file_path, temp_pdf):
                    continue

            # Add to merged PDF
            reader = PdfReader(temp_pdf)
            for page in reader.pages:
                writer.add_page(page)

        except Exception as e:
            print(f"        ERROR: {e}")


if __name__ == "__main__":
    source_directory = "/Users/ugochi141/Desktop/Largo/Got me fucked up"
    output_file = "/Users/ugochi141/Desktop/Largo/Largo_Documents_By_Conversation_Threads.pdf"

    merge_pdfs_by_threads(source_directory, output_file)

    print("\nDone!")
