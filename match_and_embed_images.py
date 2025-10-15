import base64
import os
from pathlib import Path

# Directory containing images
image_dir = Path("/Users/ugochi141/Desktop/M.S. Biotech/Fall 2025/Introduction to Bioinformatics/ACC/")
html_file = image_dir / "ACC.html"

# Based on the descriptions and timestamps, create a mapping
# We need to match based on the figure captions and likely image names
image_mapping = {
    # MSA/Alignment related images (MAFFT, MUSCLE, Clustal)
    "image1.png": "MUSCLE .png",  # Multiple Sequence Alignment - Protein (largest MUSCLE)
    "image2.png": "MAFFTMSAViewer (2).png",  # MSA Visualization 2
    "image3.png": "MUSCLE2.png",  # MSA Visualization 3
    "image4.png": "Screenshot 2025-10-12 at 1.34.30 PM.png",  # CDD Domain Architecture (largest screenshot from 1:34 PM)
    "image5.png": "Screenshot 2025-10-12 at 3.46.20 PM.png",  # Phylogenetic Tree - Unrooted
    "image6.png": "Screenshot 2025-10-12 at 3.26.39 PM.png",  # Alternative Phylogram
    "image7.png": "Screenshot 2025-10-12 at 1.35.07 PM.png",  # Detailed MSA Region (from Clustal time)
    "image8.png": "Screenshot 2025-10-12 at 3.26.29 PM.png",  # Phylogenetic Tree - Rooted
    "image9.png": "Screenshot 2025-10-12 at 3.26.15 PM.png",  # Detailed Phylogenetic Tree
    "image10.png": "Screenshot 2025-10-12 at 1.35.34 PM.png",  # Guide Tree
    "image11.png": "Screenshot 2025-10-12 at 3.26.55 PM.png",  # Radial Phylogram
    "image12.png": "Screenshot 2025-10-12 at 1.36.00 PM.png",  # Extended Guide Tree
    "image13.png": "Screenshot 2025-10-12 at 3.25.30 PM.png",  # Nucleotide Alignment 1 (largest, most detailed)
    "image14.png": "Screenshot 2025-10-12 at 3.26.04 PM.png",  # Nucleotide Alignment 2
    "image15.png": "MAFFTMSAViewer (1).png",  # Human-Rat-Mouse Comparison
    "image16.png": "Screenshot 2025-10-05 at 2.39.31 PM.png",  # Phylogram Human-Rat-Mouse
    "image17.png": "Screenshot 2025-10-05 at 3.20.16 PM.png",  # Simplified Tree
}

print("Image Mapping:")
print("=" * 80)
for placeholder, actual_file in image_mapping.items():
    filepath = image_dir / actual_file
    if filepath.exists():
        size = os.path.getsize(filepath)
        print(f"{placeholder:15} -> {actual_file:40} ({size:,} bytes)")
    else:
        print(f"{placeholder:15} -> {actual_file:40} [FILE NOT FOUND]")

print("\n" + "=" * 80)
print("Converting images to Base64 and updating HTML...")
print("=" * 80 + "\n")

# Read the HTML file
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Replace each image placeholder with base64 encoded data
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
            print(f"✓ Replaced {placeholder} with {actual_file}")
        else:
            print(f"✗ Could not find {old_src} in HTML")
    else:
        print(f"✗ File not found: {actual_file}")

# Save the updated HTML
output_file = image_dir / "ACC_with_embedded_images.html"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("\n" + "=" * 80)
print(f"✓ SUCCESS! Updated HTML saved to: {output_file}")
print("=" * 80)
print("\nThe HTML file now contains all images embedded as Base64 data URIs.")
print("You can open it in any browser and all images will display without external files.")
