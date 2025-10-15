import base64
import os

# Directory containing images
image_dir = "/Users/ugochi141/Desktop/M.S. Biotech/Fall 2025/Introduction to Bioinformatics/ACC/"
html_file = os.path.join(image_dir, "ACC.html")

# Based on visual inspection and figure captions, create the mapping
image_mapping = {
    # Figure 1 - CDD Domain Architecture
    "image4.png": "Screenshot 2025-10-12 at 1.34.30 PM.png",

    # Figures 2-5 - MSA protein alignments (MUSCLE, MAFFT)
    "image1.png": "MUSCLE .png",  # Figure 2: Multiple Sequence Alignment - 10 species
    "image7.png": "Screenshot 2025-10-12 at 1.35.07 PM.png",  # Figure 3: Detailed MSA Region
    "image2.png": "MAFFTMSAViewer (2).png",  # Figure 4: MSA Visualization 2
    "image3.png": "MUSCLE2.png",  # Figure 5: MSA Visualization 3

    # Figures 6-8, 14-17 - Phylogenetic trees
    "image5.png": "Screenshot 2025-10-12 at 3.46.20 PM.png",  # Figure 6: Unrooted tree
    "image8.png": "Screenshot 2025-10-12 at 3.26.29 PM.png",  # Figure 7: Rooted tree
    "image11.png": "Screenshot 2025-10-12 at 3.26.55 PM.png",  # Figure 8: Radial Phylogram
    "image6.png": "Screenshot 2025-10-12 at 3.26.39 PM.png",  # Figure 14: Alternative Phylogram
    "image9.png": "Screenshot 2025-10-12 at 3.26.15 PM.png",  # Figure 15: Detailed tree
    "image10.png": "Screenshot 2025-10-12 at 1.35.34 PM.png",  # Figure 16: Guide Tree
    "image12.png": "Screenshot 2025-10-12 at 1.36.00 PM.png",  # Figure 17: Extended Guide Tree

    # Figures 9-10 - Nucleotide alignments
    "image13.png": "Screenshot 2025-10-12 at 3.25.30 PM.png",  # Figure 9: Nucleotide Alignment 1
    "image14.png": "Screenshot 2025-10-12 at 3.26.04 PM.png",  # Figure 10: Nucleotide Alignment 2

    # Figures 11-13 - Human-Rat-Mouse comparisons
    "image15.png": "MAFFTMSAViewer (1).png",  # Figure 11: Human-Rat-Mouse Comparison
    "image16.png": "Screenshot 2025-10-05 at 2.39.31 PM.png",  # Figure 12: Phylogram Human-Rat-Mouse
    "image17.png": "Screenshot 2025-10-05 at 3.20.16 PM.png",  # Figure 13: Simplified Tree
}

print("=" * 80)
print("EMBEDDING IMAGES IN TP53 ANALYSIS HTML")
print("=" * 80 + "\n")

# Read the HTML file
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Replace each image placeholder with base64 encoded data
success_count = 0
failed_files = []

for placeholder, actual_file in sorted(image_mapping.items()):
    filepath = os.path.join(image_dir, actual_file)

    print(f"Processing {placeholder:12} <- {actual_file}")

    if os.path.exists(filepath):
        try:
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
                file_size = os.path.getsize(filepath)
                print(f"  ✓ SUCCESS - Embedded {len(encoded_string):,} chars ({file_size:,} bytes)\n")
                success_count += 1
            else:
                print(f"  ✗ FAILED - Placeholder not found in HTML\n")
                failed_files.append(f"{placeholder} (placeholder not in HTML)")
        except Exception as e:
            print(f"  ✗ ERROR - {str(e)}\n")
            failed_files.append(f"{placeholder} ({str(e)})")
    else:
        print(f"  ✗ FAILED - File not found: {filepath}\n")
        failed_files.append(f"{placeholder} (file not found)")

# Save the updated HTML file
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("\n" + "=" * 80)
print(f"RESULTS: Successfully embedded {success_count} of {len(image_mapping)} images")
print("=" * 80)

if success_count == len(image_mapping):
    print("\n🎉 ALL IMAGES EMBEDDED SUCCESSFULLY! 🎉")
elif success_count > 0:
    print(f"\n✓ {success_count} images embedded successfully")
    if failed_files:
        print(f"\n✗ {len(failed_files)} images failed:")
        for failed in failed_files:
            print(f"  - {failed}")
else:
    print("\n✗ NO IMAGES WERE EMBEDDED")

print(f"\nUpdated file saved to:\n{html_file}")
print("\n" + "=" * 80)
