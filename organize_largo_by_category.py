#!/usr/bin/env python3
"""
Reorganize Largo documents by category/topic instead of chronologically.
Creates a PDF with sections for each key issue area.
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
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(306, 500, title)

    # Subtitle
    if subtitle:
        c.setFont("Helvetica", 18)
        c.drawCentredString(306, 450, subtitle)

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
    c.drawCentredString(306, 670, "Organized by Topic")
    c.drawCentredString(306, 650, f"Generated: {datetime.now().strftime('%B %d, %Y')}")

    # Table of Contents
    c.setFont("Helvetica-Bold", 18)
    c.drawString(72, 600, "Table of Contents")

    y = 560
    c.setFont("Helvetica", 12)

    for idx, (category_name, files) in enumerate(categories.items(), 1):
        if y < 100:  # New page if needed
            c.showPage()
            y = 700

        c.setFont("Helvetica-Bold", 12)
        c.drawString(72, y, f"{idx}. {category_name}")
        y -= 15

        c.setFont("Helvetica", 10)
        c.drawString(90, y, f"({len(files)} documents)")
        y -= 25

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
            c.drawString(100, 700, f"Full Path: {docx_path}")
            c.save()
            return True
    except Exception as e:
        print(f"Error converting DOCX {docx_path}: {e}")
        return False


def categorize_files(source_dir):
    """Categorize files based on content and naming patterns."""

    categories = {
        "1. Leave/PTO Disputes": [],
        "2. Communication Issues with Manager": [],
        "3. Staffing Shortages & Performance Issues": [],
        "4. Blood Bank Training Requirements": [],
        "5. Daily Schedule Issues": [],
        "6. Team Chat Concerns": [],
        "7. Policy Documents": [],
        "8. Performance Analysis & Planning": [],
        "9. Other Documentation": []
    }

    # Get all files
    file_patterns = ['*.pdf', '*.png', '*.jpg', '*.jpeg', '*.docx']
    all_files = []

    for pattern in file_patterns:
        all_files.extend(glob.glob(os.path.join(source_dir, pattern)))
        all_files.extend(glob.glob(os.path.join(source_dir, '**', pattern), recursive=True))

    all_files = list(set(all_files))
    all_files.sort(key=lambda x: os.path.getmtime(x))

    # Categorize based on filename patterns
    for file_path in all_files:
        filename = os.path.basename(file_path).lower()
        categorized = False

        # PTO/Leave related
        if any(keyword in filename for keyword in ['pto', 'vacation', 'absence', 'leave', 'rejection', 'rejected']):
            categories["1. Leave/PTO Disputes"].append(file_path)
            categorized = True

        # Policy documents
        elif any(keyword in filename for keyword in ['policy', 'eeoc', 'at will', 'corrective', 'hr', 'training', 'compliant', 'cp_576']):
            categories["7. Policy Documents"].append(file_path)
            categorized = True

        # Performance/Analysis
        elif any(keyword in filename for keyword in ['performance', 'analysis', 'improvement plan', 'largo laboratory']):
            categories["8. Performance Analysis & Planning"].append(file_path)
            categorized = True

        # Schedule related
        elif 'schedule' in filename or 'scheduler' in filename:
            categories["5. Daily Schedule Issues"].append(file_path)
            categorized = True

        # Blood bank, training, investigation
        elif any(keyword in filename for keyword in ['blood', 'training', 'investigation', 'toe', 'directive']):
            categories["4. Blood Bank Training Requirements"].append(file_path)
            categorized = True

        # Lab delays, staffing
        elif any(keyword in filename for keyword in ['delay', 'staffing', 'wlu', 'credential', 'phleb']):
            categories["3. Staffing Shortages & Performance Issues"].append(file_path)
            categorized = True

        # Communication/correspondence
        elif any(keyword in filename for keyword in ['mail', 'outlook', 'correspondence', 'exchange', 'urgent']):
            categories["2. Communication Issues with Manager"].append(file_path)
            categorized = True

        # Screenshots likely contain chat/communication
        elif 'screenshot' in filename:
            # Determine based on date/time patterns
            if '8.3' in filename or '8.4' in filename:  # Evening screenshots likely chats
                categories["6. Team Chat Concerns"].append(file_path)
            elif '12.06' in filename or '5.59' in filename or '6.00' in filename:
                categories["1. Leave/PTO Disputes"].append(file_path)
            else:
                categories["2. Communication Issues with Manager"].append(file_path)
            categorized = True

        # DOCX files
        elif filename.endswith('.docx'):
            if 'evidence' in filename:
                categories["9. Other Documentation"].append(file_path)
            else:
                categories["8. Performance Analysis & Planning"].append(file_path)
            categorized = True

        # Uncategorized
        if not categorized:
            categories["9. Other Documentation"].append(file_path)

    # Remove empty categories
    categories = {k: v for k, v in categories.items() if v}

    return categories


def merge_pdfs_by_category(source_dir, output_path):
    """Main function to merge documents organized by category."""

    print("=" * 80)
    print("Largo Documents - Categorical Organization")
    print("=" * 80)
    print(f"\nScanning: {source_dir}")

    # Categorize files
    categories = categorize_files(source_dir)

    print(f"\nFound {sum(len(files) for files in categories.values())} files in {len(categories)} categories\n")

    for cat_name, files in categories.items():
        print(f"{cat_name}: {len(files)} files")

    print("\n" + "=" * 80)
    print("Processing files...\n")

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
        for category_name, files in categories.items():
            print(f"\n{category_name}")
            print("-" * 80)

            # Add section divider
            divider_pdf = create_section_divider(category_name, f"{len(files)} documents")
            reader = PdfReader(divider_pdf)
            for page in reader.pages:
                writer.add_page(page)
            os.unlink(divider_pdf)

            # Process files in this category
            for idx, file_path in enumerate(files, 1):
                file_name = os.path.basename(file_path)
                file_ext = os.path.splitext(file_path)[1].lower()
                timestamp = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')

                print(f"  {idx:3d}. [{timestamp}] {file_name}")

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
                    print(f"      ERROR: {e}")

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


if __name__ == "__main__":
    source_directory = "/Users/ugochi141/Desktop/Largo/Got me fucked up"
    output_file = "/Users/ugochi141/Desktop/Largo/Largo_Documents_By_Category.pdf"

    merge_pdfs_by_category(source_directory, output_file)

    print("\nDone!")
