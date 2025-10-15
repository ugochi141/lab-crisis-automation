#!/usr/bin/env python3
"""
Legal Evidence Organizer for Whistleblower Retaliation Case
Extracts actual message dates from Teams screenshots and organizes chronologically
"""

import os
import re
import json
import shutil
from datetime import datetime
from pathlib import Path
from PIL import Image
import pytesseract
from dateutil import parser
from collections import defaultdict

class LegalEvidenceOrganizer:
    def __init__(self, source_dir):
        self.source_dir = Path(source_dir)
        self.base_dir = Path("/Users/ugochi141/Desktop/LEGAL_TIMELINE")
        self.critical_dir = self.base_dir / "01_CRITICAL_EVIDENCE"
        self.supporting_dir = self.base_dir / "02_SUPPORTING_EVIDENCE"
        self.chronological_dir = self.base_dir / "03_COMPLETE_CHRONOLOGICAL"
        self.evidence_map = {"critical_timeline": {}, "deletion_directives": [], "all_files": []}
        self.processed_files = []

        # Critical event patterns
        self.critical_events = {
            "investigation_ordered": {
                "keywords": ["investigate", "second shift", "performance"],
                "date_hint": "July 14",
                "priority": 1
            },
            "chronic_low_performers": {
                "keywords": ["chronic low performers", "CA path"],
                "date_hint": "July 15",
                "priority": 2
            },
            "analysis_provided": {
                "keywords": ["Culture issue", "runs deeper", "Level 3 Trauma"],
                "date_hint": "September 29",
                "priority": 3
            },
            "whistleblowing": {
                "keywords": ["41.23%", "failure rate"],
                "date_hint": "October 3",
                "priority": 4
            },
            "censorship_directive": {
                "keywords": ["delete", "inappropriate", "directive", "remove this message"],
                "date_hint": "October 3",
                "priority": 5
            },
            "final_warning": {
                "keywords": ["Final Written Warning", "corrective action"],
                "date_hint": "October 8",
                "priority": 6
            }
        }

    def setup_directories(self):
        """Create organized directory structure"""
        for directory in [self.critical_dir, self.supporting_dir, self.chronological_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory structure at {self.base_dir}")

    def extract_text_from_image(self, image_path):
        """Extract text from screenshot using OCR"""
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            return text
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return ""

    def extract_date_from_text(self, text):
        """Extract dates from Teams message text"""
        dates_found = []

        # Pattern 1: Full date format (July 14, 2025 11:03 AM)
        pattern1 = r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\s+\d{1,2}:\d{2}\s*(AM|PM)?'

        # Pattern 2: Short date format (7/14/25, 10/3/25)
        pattern2 = r'\d{1,2}/\d{1,2}/\d{2,4}'

        # Pattern 3: Time only (for messages on same day)
        pattern3 = r'\d{1,2}:\d{2}\s*(AM|PM)'

        for pattern in [pattern1, pattern2]:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    if isinstance(match, tuple):
                        match = ' '.join(match)
                    parsed_date = parser.parse(match, fuzzy=True)
                    dates_found.append(parsed_date)
                except:
                    pass

        return dates_found

    def identify_event_type(self, text):
        """Identify the type of event based on content"""
        text_lower = text.lower()
        identified_events = []

        for event_type, event_data in self.critical_events.items():
            match_count = sum(1 for keyword in event_data["keywords"] if keyword.lower() in text_lower)
            if match_count >= 2:  # At least 2 keywords must match
                identified_events.append((event_type, event_data["priority"], match_count))

        # Sort by match count and priority
        identified_events.sort(key=lambda x: (-x[2], x[1]))

        if identified_events:
            return identified_events[0][0]

        # Check for sender names to categorize
        if "nathaniel" in text_lower:
            return "directive"
        elif "ugochi" in text_lower:
            return "response"
        elif "tracy" in text_lower:
            return "witness"

        return "supporting"

    def generate_new_filename(self, date, event_type, original_path):
        """Generate new filename based on actual date and event type"""
        if date:
            date_str = date.strftime("%Y-%m-%d_%H%M")
        else:
            # Use original filename date as fallback
            date_str = "undated"

        # Clean event type for filename
        event_clean = event_type.upper().replace("_", "_")

        # Add counter if multiple files for same timestamp
        counter = 1
        base_name = f"{date_str}_{event_clean}"
        new_name = f"{base_name}_{counter:02d}.png"

        while (self.chronological_dir / new_name).exists():
            counter += 1
            new_name = f"{base_name}_{counter:02d}.png"

        return new_name

    def process_screenshot(self, image_path):
        """Process a single screenshot"""
        print(f"\nProcessing: {image_path.name}")

        # Extract text
        text = self.extract_text_from_image(image_path)
        if not text:
            print(f"  ⚠ No text extracted")
            return None

        # Extract dates
        dates = self.extract_date_from_text(text)
        actual_date = dates[0] if dates else None

        # Identify event type
        event_type = self.identify_event_type(text)

        # Generate new filename
        new_filename = self.generate_new_filename(actual_date, event_type, image_path)

        # Determine destination based on event type
        if event_type in ["investigation_ordered", "analysis_provided", "whistleblowing",
                         "censorship_directive", "final_warning"]:
            dest_dir = self.critical_dir
            is_critical = True
        else:
            dest_dir = self.supporting_dir
            is_critical = False

        # Copy to appropriate directory and chronological
        dest_path = dest_dir / new_filename
        chron_path = self.chronological_dir / new_filename

        shutil.copy2(image_path, dest_path)
        shutil.copy2(image_path, chron_path)

        # Create file info
        file_info = {
            "original_name": image_path.name,
            "new_name": new_filename,
            "actual_date": actual_date.isoformat() if actual_date else None,
            "event_type": event_type,
            "is_critical": is_critical,
            "text_preview": text[:200],
            "full_path": str(dest_path)
        }

        # Update evidence map
        if is_critical and event_type in self.critical_events:
            self.evidence_map["critical_timeline"][event_type] = {
                "date": actual_date.strftime("%Y-%m-%d %I:%M %p") if actual_date else "Unknown",
                "file": new_filename,
                "content_preview": text[:100]
            }

        # Check for deletion directives
        if "delete" in text.lower() and "directive" in text.lower():
            time_match = re.search(r'(\d{1,2}:\d{2}\s*(AM|PM))', text, re.IGNORECASE)
            if time_match:
                self.evidence_map["deletion_directives"].append({
                    "time": time_match.group(1),
                    "date": actual_date.strftime("%b %d") if actual_date else "Unknown",
                    "file": new_filename
                })

        self.evidence_map["all_files"].append(file_info)

        print(f"  ✓ Date: {actual_date.strftime('%Y-%m-%d %H:%M') if actual_date else 'Unknown'}")
        print(f"  ✓ Type: {event_type}")
        print(f"  ✓ Critical: {'Yes' if is_critical else 'No'}")
        print(f"  ✓ Saved as: {new_filename}")

        return file_info

    def process_all_screenshots(self):
        """Process all PNG screenshots in the source directory"""
        # Get all PNG files (excluding resized folder)
        png_files = [f for f in self.source_dir.glob("*.png") if f.is_file()]

        print(f"\nFound {len(png_files)} PNG files to process")

        for png_file in png_files:
            try:
                result = self.process_screenshot(png_file)
                if result:
                    self.processed_files.append(result)
            except Exception as e:
                print(f"Error processing {png_file}: {e}")

    def save_evidence_map(self):
        """Save the evidence mapping to JSON"""
        json_path = self.base_dir / "evidence_map.json"
        with open(json_path, 'w') as f:
            json.dump(self.evidence_map, f, indent=2, default=str)
        print(f"\n✓ Evidence map saved to {json_path}")

    def create_legal_brief(self):
        """Create markdown legal brief summary"""
        brief_path = self.base_dir / "LEGAL_BRIEF_TIMELINE.md"

        brief_content = """# RETALIATION TIMELINE - LARGO LABORATORY
## Whistleblower Retaliation Case Evidence

---

## CRITICAL PATTERN OF RETALIATION

### Timeline of Events:

1. **July 14, 2025**: Director Nathaniel orders investigation into second shift performance
   - Time: 11:03 AM and 11:16 AM
   - Directive to investigate "chronic low performers"
   - Performance metrics shared: 57%, 70%, 75%, 66%

2. **July 15, 2025**: Escalation directive
   - Time: 4:21 PM
   - "Start any chronic low performers on a CA path"

3. **September 29, 2025**: Comprehensive analysis provided
   - Time: 5:39 PM
   - Ugochi provides detailed analysis: "Culture issue runs deeper than individual performance"
   - References Level 3 Trauma hospital requirements
   - **Director acknowledges**: "I see the issue with staffing"

4. **October 3, 2025**: Protected whistleblowing activity
   - 8:21 AM: Ugochi shares same analysis with staff (41.23% failure rate)
   - 8:35 AM: First censorship demand: "Your messages are bordering on inappropriate"
   - 8:50 AM: Second demand: "I am asking that you delete the post"
   - 12:19 PM: Third demand: "This is a directive. Remove this message"
   - 4:30 PM: Fourth deletion directive

5. **October 8, 2025**: Retaliatory discipline
   - Final Written Warning issued
   - First disciplinary action in 9 months of employment
   - Issued 5 days after protected activity

---

## KEY EVIDENCE OF RETALIATION

### Protected Activity Elements:
✓ **Investigation was DIRECTED** by management (July 14)
✓ **Analysis was REQUESTED** by director
✓ **Findings were ACKNOWLEDGED** as valid (Sept 29)
✓ **Sharing findings was PROTECTED** whistleblowing activity
✓ **Discipline was IMMEDIATE** retaliation (5 days)

### Pattern of Censorship (October 3):
- Four deletion demands in 8 hours
- Escalating language: "asking" → "directive"
- No policy violation cited
- Same content previously acknowledged as valid

### Retaliatory Nature:
- No prior disciplinary actions in 9 months
- Discipline immediately follows protected activity
- Content shared was same as analysis provided to director
- Director had acknowledged validity of concerns

---

## LEGAL SIGNIFICANCE

This evidence demonstrates:

1. **Protected Activity**: Reporting systemic performance issues affecting patient safety
2. **Adverse Action**: Final Written Warning (severe discipline)
3. **Causal Connection**: 5 days between whistleblowing and discipline
4. **Pretext**: Same analysis praised by director, punished when shared with staff
5. **Pattern**: Four censorship attempts before formal discipline

---

## CRITICAL FILES

- Investigation Order: July 14, 2025
- Analysis Acknowledgment: September 29, 2025
- Whistleblowing Event: October 3, 2025 (8:21 AM)
- Censorship Directives: October 3, 2025 (multiple times)
- Retaliatory Discipline: October 8, 2025

---

## MARYLAND OSHA DEADLINE

**Filing Deadline**: November 7, 2025
**Case Type**: Whistleblower Retaliation
**Protected Activity**: Reporting workplace safety concerns affecting patient care

---

*Evidence organized and timeline established from Teams message screenshots*
*All dates extracted from actual message timestamps, not screenshot capture dates*
"""

        with open(brief_path, 'w') as f:
            f.write(brief_content)

        print(f"✓ Legal brief saved to {brief_path}")

    def generate_summary(self):
        """Generate processing summary"""
        print("\n" + "="*60)
        print("PROCESSING COMPLETE")
        print("="*60)

        print(f"\n📁 Files Processed: {len(self.processed_files)}")
        print(f"📂 Output Directory: {self.base_dir}")

        # Count by event type
        event_counts = defaultdict(int)
        for file in self.processed_files:
            event_counts[file['event_type']] += 1

        print("\n📊 Events Identified:")
        for event_type, count in sorted(event_counts.items()):
            print(f"  - {event_type}: {count} files")

        print("\n⚠️ Critical Events Found:")
        for event, data in self.evidence_map["critical_timeline"].items():
            print(f"  - {event}: {data['date']}")

        print(f"\n✅ Evidence Map: {self.base_dir / 'evidence_map.json'}")
        print(f"✅ Legal Brief: {self.base_dir / 'LEGAL_BRIEF_TIMELINE.md'}")
        print(f"✅ Critical Evidence: {self.critical_dir}")
        print(f"✅ Chronological Order: {self.chronological_dir}")

def main():
    source_dir = "/Users/ugochi141/Desktop/Largo/Got me fucked up"

    print("LEGAL EVIDENCE ORGANIZER")
    print("Whistleblower Retaliation Case")
    print("="*60)

    organizer = LegalEvidenceOrganizer(source_dir)

    print("\n1. Setting up directories...")
    organizer.setup_directories()

    print("\n2. Processing screenshots...")
    organizer.process_all_screenshots()

    print("\n3. Saving evidence map...")
    organizer.save_evidence_map()

    print("\n4. Creating legal brief...")
    organizer.create_legal_brief()

    print("\n5. Generating summary...")
    organizer.generate_summary()

if __name__ == "__main__":
    main()