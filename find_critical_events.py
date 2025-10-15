#!/usr/bin/env python3
"""
Quick Critical Event Finder - Targeted search for key evidence
"""

import os
import re
import json
from pathlib import Path
from PIL import Image
import pytesseract
from datetime import datetime

def quick_ocr(image_path, max_size=(1200, 1200)):
    """Quick OCR with image resizing for speed"""
    try:
        img = Image.open(image_path)
        # Resize for faster OCR
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Error: {e}")
        return ""

def find_critical_messages():
    """Find specific critical messages in screenshots"""
    source_dir = Path("/Users/ugochi141/Desktop/Largo/Got me fucked up")
    output_dir = Path("/Users/ugochi141/Desktop/CRITICAL_EVIDENCE_QUICK")
    output_dir.mkdir(exist_ok=True)

    # Critical search patterns
    critical_searches = [
        {
            "name": "July_14_Investigation",
            "patterns": ["investigate", "second shift", "performance"],
            "date_pattern": r"July 14.*2025|7/14/25"
        },
        {
            "name": "Sept_29_Analysis",
            "patterns": ["Culture issue", "runs deeper", "Level 3"],
            "date_pattern": r"September 29.*2025|Sept 29.*2025|9/29/25"
        },
        {
            "name": "Oct_3_Whistleblowing",
            "patterns": ["41.23%", "failure rate"],
            "date_pattern": r"October 3.*2025|Oct 3.*2025|10/3/25"
        },
        {
            "name": "Oct_3_Censorship",
            "patterns": ["delete", "inappropriate", "directive", "remove this message"],
            "date_pattern": r"October 3.*2025|Oct 3.*2025|10/3/25"
        },
        {
            "name": "Oct_8_Warning",
            "patterns": ["Final Written Warning", "corrective action"],
            "date_pattern": r"October 8.*2025|Oct 8.*2025|10/8/25"
        }
    ]

    results = {
        "critical_events_found": {},
        "files_processed": 0,
        "matches": []
    }

    # Get all PNG files
    png_files = list(source_dir.glob("*.png"))[:50]  # Process first 50 for speed

    print(f"Searching {len(png_files)} files for critical events...")
    print("="*60)

    for i, png_file in enumerate(png_files, 1):
        print(f"\r[{i}/{len(png_files)}] Scanning: {png_file.name[:40]:<40}", end="")

        text = quick_ocr(png_file)
        if not text:
            continue

        text_lower = text.lower()
        results["files_processed"] += 1

        # Check each critical event
        for search in critical_searches:
            # Check if keywords match
            keyword_matches = sum(1 for pattern in search["patterns"] if pattern.lower() in text_lower)

            if keyword_matches >= 2:  # At least 2 keywords
                # Extract date if possible
                date_match = re.search(search["date_pattern"], text, re.IGNORECASE)
                date_str = date_match.group(0) if date_match else "Date not found"

                # Extract time if possible
                time_match = re.search(r'(\d{1,2}:\d{2}\s*(AM|PM))', text, re.IGNORECASE)
                time_str = time_match.group(0) if time_match else ""

                # Extract snippet around keywords
                snippet = ""
                for pattern in search["patterns"]:
                    pattern_match = re.search(f'.{{0,50}}{re.escape(pattern)}.{{0,50}}', text, re.IGNORECASE | re.DOTALL)
                    if pattern_match:
                        snippet = pattern_match.group(0).replace('\n', ' ')[:200]
                        break

                event_key = search["name"]
                if event_key not in results["critical_events_found"]:
                    results["critical_events_found"][event_key] = []

                results["critical_events_found"][event_key].append({
                    "file": png_file.name,
                    "date": date_str,
                    "time": time_str,
                    "snippet": snippet,
                    "matches": keyword_matches
                })

                # Copy critical file
                import shutil
                dest_name = f"{search['name']}_{len(results['critical_events_found'][event_key]):02d}_{png_file.name}"
                dest_path = output_dir / dest_name
                shutil.copy2(png_file, dest_path)

                print(f"\n✓ FOUND: {search['name']} in {png_file.name}")
                print(f"  Date: {date_str} {time_str}")
                print(f"  Preview: {snippet[:100]}...")

    # Save results
    results_file = output_dir / "critical_events_summary.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    # Print summary
    print("\n\n" + "="*60)
    print("CRITICAL EVENTS SUMMARY")
    print("="*60)

    for event_name, matches in results["critical_events_found"].items():
        print(f"\n{event_name}:")
        for match in matches:
            print(f"  • {match['file']}")
            print(f"    Date/Time: {match['date']} {match['time']}")

    print(f"\n✓ Files processed: {results['files_processed']}")
    print(f"✓ Critical events found: {len(results['critical_events_found'])}")
    print(f"✓ Output folder: {output_dir}")
    print(f"✓ Summary saved: {results_file}")

    return results

if __name__ == "__main__":
    find_critical_messages()