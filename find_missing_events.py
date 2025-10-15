#!/usr/bin/env python3
"""
Find specific missing critical events
"""

import os
import re
from pathlib import Path
from PIL import Image
import pytesseract
import shutil

def search_for_specific_events():
    """Search for 41.23% whistleblowing and Final Written Warning"""
    source_dir = Path("/Users/ugochi141/Desktop/Largo/Got me fucked up")
    output_dir = Path("/Users/ugochi141/Desktop/CRITICAL_EVIDENCE_QUICK")

    # Specific searches
    searches = [
        {
            "name": "Oct_3_Whistleblowing_41percent",
            "patterns": ["41.23", "41%", "failure", "rate"],
            "priority": 1
        },
        {
            "name": "Oct_8_Final_Warning",
            "patterns": ["Final Written Warning", "written warning", "corrective action", "CA"],
            "priority": 2
        }
    ]

    # Get all PNG files we haven't searched yet
    png_files = list(source_dir.glob("*.png"))

    print(f"Searching {len(png_files)} files for missing critical events...")
    print("Looking for: 41.23% failure rate and Final Written Warning")
    print("="*60)

    found_events = []

    for i, png_file in enumerate(png_files, 1):
        print(f"\r[{i}/{len(png_files)}] Scanning: {png_file.name[:40]:<40}", end="")

        try:
            # Quick OCR
            img = Image.open(png_file)
            img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
            text = pytesseract.image_to_string(img)
            text_lower = text.lower()

            for search in searches:
                # Check patterns
                matches = [p for p in search["patterns"] if p.lower() in text_lower]

                if len(matches) >= 2:
                    # Extract context
                    snippet = ""
                    for pattern in matches:
                        pattern_regex = re.escape(pattern)
                        match = re.search(f'.{{0,100}}{pattern_regex}.{{0,100}}', text, re.IGNORECASE | re.DOTALL)
                        if match:
                            snippet = match.group(0).replace('\n', ' ')
                            break

                    # Extract date/time
                    date_match = re.search(r'(10/3/25|10/8/25|October [38].*2025)', text, re.IGNORECASE)
                    time_match = re.search(r'(\d{1,2}:\d{2}\s*(AM|PM))', text, re.IGNORECASE)

                    event = {
                        "file": png_file.name,
                        "event": search["name"],
                        "date": date_match.group(0) if date_match else "Date not found",
                        "time": time_match.group(0) if time_match else "",
                        "snippet": snippet[:200],
                        "patterns_found": matches
                    }

                    found_events.append(event)

                    # Copy file
                    dest_name = f"{search['name']}_{png_file.name}"
                    dest_path = output_dir / dest_name
                    shutil.copy2(png_file, dest_path)

                    print(f"\n✓ FOUND: {search['name']}")
                    print(f"  File: {png_file.name}")
                    print(f"  Date/Time: {event['date']} {event['time']}")
                    print(f"  Patterns: {', '.join(matches)}")
                    print(f"  Context: {snippet[:100]}...")

        except Exception as e:
            continue

    # Print summary
    print("\n\n" + "="*60)
    print("MISSING EVENTS SEARCH RESULTS")
    print("="*60)

    if found_events:
        for event in found_events:
            print(f"\n{event['event']}:")
            print(f"  File: {event['file']}")
            print(f"  Date: {event['date']} {event['time']}")
            print(f"  Found: {', '.join(event['patterns_found'])}")
    else:
        print("\n⚠ The missing events were not found in the scanned files.")
        print("They may be in:")
        print("  - Other screenshots not yet scanned")
        print("  - PDF files in the folder")
        print("  - The 'resized' subfolder")

    print(f"\n✓ Files searched: {len(png_files)}")
    print(f"✓ Events found: {len(found_events)}")

    return found_events

if __name__ == "__main__":
    search_for_specific_events()