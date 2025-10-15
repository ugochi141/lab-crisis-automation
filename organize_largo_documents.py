#!/usr/bin/env python3
"""
Organize all documents and images from Largo folder into a single PDF
ordered by modification date and time.
"""

import os
import glob
from datetime import datetime
from pathlib import Path
import subprocess
import tempfile
import shutil

# Try to import required libraries
try:
    from PIL import Image
    import img2pdf
except ImportError:
    print("Installing required packages...")
    subprocess.run(["pip", "install", "pillow", "img2pdf", "pypdf"], check=True)
    from PIL import Image
    import img2pdf

try:
    from pypdf import PdfWriter, PdfReader
except ImportError:
    subprocess.run(["pip", "install", "pypdf"], check=True)
    from pypdf import PdfWriter, PdfReader

try:
    from docx2pdf import convert as docx2pdf_convert
    DOCX2PDF_AVAILABLE = True
except ImportError:
    print("Note: docx2pdf not available on macOS. Will use alternative method for DOCX files.")
    DOCX2PDF_AVAILABLE = False


def get_files_sorted_by_time(directory):
    """Get all document and image files sorted by modification time."""
    file_patterns = ['*.pdf', '*.png', '*.jpg', '*.jpeg', '*.docx']
    files = []

    for pattern in file_patterns:
        # Search in main directory and subdirectories
        files.extend(glob.glob(os.path.join(directory, pattern)))
        files.extend(glob.glob(os.path.join(directory, '**', pattern), recursive=True))

    # Remove duplicates and get file info
    files = list(set(files))

    # Sort by modification time
    files_with_time = []
    for file_path in files:
        if os.path.isfile(file_path):
            mtime = os.path.getmtime(file_path)
            files_with_time.append((mtime, file_path))

    files_with_time.sort(key=lambda x: x[0])

    return files_with_time


def convert_image_to_pdf(image_path, output_pdf):
    """Convert an image to PDF."""
    try:
        # Open and convert image
        img = Image.open(image_path)

        # Convert to RGB if necessary
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # Save as PDF
        img.save(output_pdf, 'PDF', resolution=100.0)
        return True
    except Exception as e:
        print(f"Error converting image {image_path}: {e}")
        return False


def convert_docx_to_pdf_mac(docx_path, output_pdf):
    """Convert DOCX to PDF on macOS using textutil or LibreOffice."""
    try:
        # Try using LibreOffice if available
        result = subprocess.run(
            ['which', 'soffice'],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            # LibreOffice is available
            temp_dir = tempfile.mkdtemp()
            subprocess.run([
                'soffice',
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', temp_dir,
                docx_path
            ], check=True, capture_output=True)

            # Find the generated PDF
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
            print(f"LibreOffice not found. Creating placeholder for {docx_path}")
            # Create a placeholder PDF with the filename
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter

            c = canvas.Canvas(output_pdf, pagesize=letter)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(100, 750, "DOCX Document (Conversion Not Available)")
            c.setFont("Helvetica", 12)
            c.drawString(100, 720, f"Filename: {os.path.basename(docx_path)}")
            c.drawString(100, 700, f"Full Path: {docx_path}")
            c.drawString(100, 680, "Please convert this document manually if needed.")
            c.save()
            return True

    except Exception as e:
        print(f"Error converting DOCX {docx_path}: {e}")
        return False


def merge_pdfs_chronologically(source_dir, output_path):
    """Main function to merge all documents into a single PDF."""

    print(f"Scanning directory: {source_dir}")
    files_with_time = get_files_sorted_by_time(source_dir)

    print(f"\nFound {len(files_with_time)} files to process")
    print("=" * 80)

    # Create temporary directory for converted files
    temp_dir = tempfile.mkdtemp()
    temp_pdfs = []

    try:
        # Convert all files to PDF
        for idx, (mtime, file_path) in enumerate(files_with_time, 1):
            file_name = os.path.basename(file_path)
            file_ext = os.path.splitext(file_path)[1].lower()
            timestamp = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')

            print(f"{idx:3d}. [{timestamp}] {file_name}")

            temp_pdf = os.path.join(temp_dir, f"{idx:03d}_{file_name}.pdf")

            if file_ext == '.pdf':
                # Copy PDF directly
                shutil.copy2(file_path, temp_pdf)
                temp_pdfs.append(temp_pdf)

            elif file_ext in ['.png', '.jpg', '.jpeg']:
                # Convert image to PDF
                if convert_image_to_pdf(file_path, temp_pdf):
                    temp_pdfs.append(temp_pdf)
                else:
                    print(f"   -> Failed to convert image")

            elif file_ext == '.docx':
                # Convert DOCX to PDF
                if convert_docx_to_pdf_mac(file_path, temp_pdf):
                    temp_pdfs.append(temp_pdf)
                else:
                    print(f"   -> Failed to convert DOCX")

        print("\n" + "=" * 80)
        print(f"Successfully prepared {len(temp_pdfs)} PDFs for merging")
        print("\nMerging all PDFs into final document...")

        # Merge all PDFs using PdfWriter
        writer = PdfWriter()

        for pdf_path in temp_pdfs:
            try:
                reader = PdfReader(pdf_path)
                for page in reader.pages:
                    writer.add_page(page)
            except Exception as e:
                print(f"Warning: Could not merge {os.path.basename(pdf_path)}: {e}")

        # Write merged PDF
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        print(f"\nSuccess! Created merged PDF: {output_path}")
        print(f"Total pages: {len(writer.pages)}")

        # Get file size
        file_size = os.path.getsize(output_path)
        file_size_mb = file_size / (1024 * 1024)
        print(f"File size: {file_size_mb:.2f} MB")

    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)

    return output_path


if __name__ == "__main__":
    source_directory = "/Users/ugochi141/Desktop/Largo/Got me fucked up"
    output_file = "/Users/ugochi141/Desktop/Largo/Largo_Documents_Chronological.pdf"

    print("Largo Documents Organizer")
    print("=" * 80)
    print(f"Source: {source_directory}")
    print(f"Output: {output_file}")
    print("=" * 80 + "\n")

    # Check if reportlab is available for DOCX placeholder
    try:
        import reportlab
    except ImportError:
        print("Installing reportlab for DOCX placeholders...")
        subprocess.run(["pip", "install", "reportlab"], check=True)

    merge_pdfs_chronologically(source_directory, output_file)

    print("\n" + "=" * 80)
    print("Done!")
    print("=" * 80)
