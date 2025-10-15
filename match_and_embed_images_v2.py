import base64
import os
from pathlib import Path

# Directory containing images
image_dir = Path("/Users/ugochi141/Desktop/M.S. Biotech/Fall 2025/Introduction to Bioinformatics/ACC/")
html_file = image_dir / "ACC.html"

# Based on visual inspection and figure captions, create the mapping
image_mapping = {
    # Figure 1 - CDD Domain Architecture
    "image4.png": "Screenshot 2025-10-12 at 1.34.30 PM.png",

    # Figures 2-5 - MSA protein alignments (MUSCLE, MAFFT)
    "image1.png": "MUSCLE .png",  # Figure 2: Multiple Sequence Alignment - 10 species, Clustal2 color
    "image7.png": "Screenshot 2025-10-12 at 1.35.07 PM.png",  # Figure 3: Detailed MSA Region
    "image2.png": "MAFFTMSAViewer (2).png",  # Figure 4: MSA Visualization 2 (large MAFFT)
    "image3.png": "MUSCLE2.png",  # Figure 5: MSA Visualization 3 (Extended MUSCLE view)

    # Figures 6-8, 14-17 - Phylogenetic trees
    "image5.png": "Screenshot 2025-10-12 at 3.46.20 PM.png",  # Figure 6: Phylogenetic Tree - Unrooted
    "image8.png": "Screenshot 2025-10-12 at 3.26.29 PM.png",  # Figure 7: Phylogenetic Tree - Rooted
    "image11.png": "Screenshot 2025-10-12 at 3.26.55 PM.png",  # Figure 8: Radial Phylogram
    "image6.png": "Screenshot 2025-10-12 at 3.26.39 PM.png",  # Figure 14: Alternative Phylogram
    "image9.png": "Screenshot 2025-10-12 at 3.26.15 PM.png",  # Figure 15: Detailed Phylogenetic Tree
    "image10.png": "Screenshot 2025-10-12 at 1.35.34 PM.png",  # Figure 16: Guide Tree
    "image12.png": "Screenshot 2025-10-12 at 1.36.00 PM.png",  # Figure 17: Extended Guide Tree (3 species)

    # Figures 9-10 - Nucleotide alignments
    "image13.png": "Screenshot 2025-10-12 at 3.25.30 PM.png",  # Figure 9: Nucleotide Alignment 1 (largest)
    "image14.png": "Screenshot 2025-10-12 at 3.26.04 PM.png",  # Figure 10: Nucleotide Alignment 2

    # Figures 11-13 - Human-Rat-Mouse comparisons
    "image15.png": "MAFFTMSAViewer (1).png",  # Figure 11: Human-Rat-Mouse Comparison (small MAFFT)
    "image16.png": "Screenshot 2025-10-05 at 2.39.31 PM.png",  # Figure 12: Phylogram Human-Rat-Mouse
    "image17.png": "Screenshot 2025-10-05 at 3.20.16 PM.png",  # Figure 13: Simplified Tree (3 species)
}

print("=" * 80)
print("IMAGE MAPPING FOR TP53 ANALYSIS HTML")
print("=" * 80)
print("\nMapping placeholders to actual files:")
print("-" * 80)

for placeholder, actual_file in sorted(image_mapping.items()):
    filepath = image_dir / actual_file
    if filepath.exists():
        size = os.path.getsize(filepath)
        print(f"{placeholder:15} -> {actual_file:45} ({size:>9,} bytes)")
    else:
        print(f"{placeholder:15} -> {actual_file:45} [FILE NOT FOUND]")

print("\n" + "=" * 80)
print("CONVERTING IMAGES TO BASE64 AND UPDATING HTML")
print("=" * 80 + "\n")

# Read the HTML file
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Replace each image placeholder with base64 encoded data
success_count = 0
for placeholder, actual_file in image_mapping.items():
    filepath = image_dir / actual_file

    if filepath.exists():
        # Read and encode the image
        with open(filepath, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        # Determine image type
        file_ext = actual_file.lower().split('.')[-1]
        mime_type = f"image/{file_ext}"

        # Create the data URI
        data_uri = f"data:{mime_type};base64,{encoded_string}"

        # Replace in HTML
        old_src = f'src="{placeholder}"'
        new_src = f'src="{data_uri}"'

        if old_src in html_content:
            html_content = html_content.replace(old_src, new_src)
            print(f"✓ Embedded {placeholder:12} ({len(encoded_string):>9,} chars) <- {actual_file}")
            success_count += 1
        else:
            print(f"✗ Could not find placeholder {placeholder} in HTML")
    else:
        print(f"✗ File not found: {actual_file}")

# Save the updated HTML file (replace the original)
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("\n" + "=" * 80)
print(f"✓✓✓ SUCCESS! Embedded {success_count} of {len(image_mapping)} images")
print("=" * 80)
print(f"\nUpdated file: {html_file}")
print("\nAll images are now embedded as Base64 data URIs.")
print("The HTML file is now completely self-contained!")
print("\nYou can:")
print("  • Open it in any browser")
print("  • Share it as a single file")
print("  • View it offline without external image files")
print("=" * 80)
