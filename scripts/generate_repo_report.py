#!/usr/bin/env python3
"""Generate repository report"""

import json
from pathlib import Path
from datetime import datetime

def main():
    print("Generating repository report...")
    
    # Load analysis if exists
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    analysis_file = reports_dir / "repo_analysis.json"
    if analysis_file.exists():
        with open(analysis_file, 'r') as f:
            data = json.load(f)
        print(f"✓ Loaded analysis for {len(data.get('repositories', []))} repositories")
    else:
        # Create basic report
        data = {
            "timestamp": datetime.now().isoformat(),
            "repositories": [],
            "summary": {"total_repositories": 0},
            "recommendations": []
        }
    
    # Save report
    with open(reports_dir / "repo_report.json", 'w') as f:
        json.dump(data, f, indent=2)
    
    print("✓ Repository report generated")
    return 0

if __name__ == "__main__":
    exit(main())