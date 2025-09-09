#!/usr/bin/env python3
"""
Generate Repository Report
Creates a comprehensive report from repository analysis
"""

import json
from pathlib import Path
from datetime import datetime

def generate_report():
    """Generate HTML report from repository analysis"""
    
    # Load analysis data
    analysis_file = Path("reports/repo_analysis.json")
    if not analysis_file.exists():
        print("No repository analysis found - running basic report")
        # Create basic report
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "repositories": [],
            "summary": {"total_repositories": 0, "healthy": 0}
        }
    else:
        with open(analysis_file, 'r') as f:
            report_data = json.load(f)
    
    # Generate simple text report
    print(f"Repository Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    summary = report_data.get("summary", {})
    print(f"Total Repositories: {summary.get('total_repositories', 0)}")
    print(f"Healthy: {summary.get('healthy', 0)}")
    print(f"Needs Attention: {summary.get('needs_attention', 0)}")
    
    # Save summary
    with open('repo_report_summary.txt', 'w') as f:
        f.write(f"Repository Analysis Report\n")
        f.write(f"Generated: {datetime.now()}\n")
        f.write(f"Total: {summary.get('total_repositories', 0)}\n")
        f.write(f"Healthy: {summary.get('healthy', 0)}\n")
    
    print("✓ Repository report generated")
    return 0

def main():
    """Main function"""
    return generate_report()

if __name__ == "__main__":
    exit(main())