#!/usr/bin/env python3
"""
Standard Operating Procedure (SOP) Generator
Creates comprehensive SOPs following Kaiser Permanente laboratory standards
"""

import os
import json
from datetime import datetime
from pathlib import Path

class SOPGenerator:
    """Generate standardized laboratory SOPs"""
    
    def __init__(self):
        self.sop_structure = [
            "PURPOSE",
            "CLINICAL SIGNIFICANCE", 
            "SCOPE",
            "RESPONSIBILITIES",
            "SAFETY REQUIREMENTS",
            "SPECIMEN REQUIREMENTS",
            "REAGENTS AND SUPPLIES",
            "EQUIPMENT",
            "MAINTENANCE",
            "QUALITY CONTROL REQUIREMENTS",
            "CALIBRATION",
            "TROUBLESHOOTING", 
            "TEST PROCEDURE",
            "CALCULATIONS AND RESULT REPORTING",
            "REFERENCE RANGES",
            "CRITICAL VALUES",
            "LIMITATIONS AND INTERFERENCES",
            "EMERGENCY PROCEDURES",
            "TECHNICAL SUPPORT",
            "QUALITY ASSURANCE",
            "REGULATORY COMPLIANCE",
            "DOWNTIME PROCEDURES",
            "REFERENCES"
        ]
        
        self.standard_components = self.load_standard_components()
    
    def load_standard_components(self):
        """Load standard SOP components"""
        return {
            "qc_failure_actions": """
QC Failure Actions:
1. Repeat QC analysis
2. Check reagent expiration dates
3. Inspect instrument for problems
4. Contact manager if QC continues to fail
5. Do NOT report patient results until QC is acceptable
""",
            "documentation_requirements": """
Documentation Retention:
Document Type                    Retention Period
Patient results                  2 years minimum
Quality control records          2 years
Instrument maintenance          2 years
Personnel records               2 years post-employment
Proficiency testing             2 years
""",
            "documentation_policy": """
⚠️ One Strike Policy for Documentation Mistakes
Documentation errors are treated with utmost seriousness to maintain laboratory integrity and patient safety.

Usage of Proper Documentation Tools:
* Electronic Records: All entries must be made in approved LIS/EMR systems
* Corrections: Single line through error, initial, date, and reason for change
* No Erasures: Never use white-out, erasers, or delete electronic entries
* Contemporaneous: Document in real-time, never pre or post-date
* Complete Entries: All fields must be completed; use "N/A" if not applicable
* Audit Trail: All electronic changes tracked automatically
""",
            "critical_qc_rule": """
⚠️ Critical QC Rule:
NEVER report patient results if QC is not acceptable. Patient safety depends on accurate results. If QC fails, troubleshoot and repeat. If still failing, use backup method or send to reference lab.

Follow-up Notification Requirements:
1. Immediately notify Lead Technologist of QC failure
2. Document all troubleshooting steps attempted
3. Contact Technical Support and obtain reference number
4. Notify Technical Quality Specialist with:
   * All troubleshooting steps performed
   * Tech support reference number
   * Current instrument status
5. Notify Laboratory Manager with complete documentation

CRITICAL: Before contacting Technical Quality Specialist and Lab Manager, ensure you have documented all troubleshooting steps and obtained the reference number from Tech Support.
""",
            "tat_requirements": """
Turnaround Time (TAT) Requirements:
Priority    TAT Goal       Measured From              Compliance Target
STAT       60 minutes     Receipt in lab to result   ≥90%
Urgent     2 hours        Receipt in lab to result   ≥90%
Routine    4 hours        Receipt in lab to result   ≥85%
Critical Values 30 minutes Result verification to notification 100%

⏱️ STAT Specimens:
* Target TAT: 60 minutes from receipt in laboratory
* Critical values must be called within 30 minutes of result
* ED and ICU specimens receive priority processing

📋 Routine Specimens:
* Target TAT: 4 hours from receipt in laboratory
* Outpatient specimens: Results available same day if received before 2:00 PM

TAT Monitoring:
* TAT is monitored monthly and reported to laboratory management
* TAT begins when specimen is received in laboratory (time-stamped)
* TAT ends when result is verified and released in LIS
* Target compliance: ≥90% for STAT, ≥95% for routine
""",
            "emergency_procedures": """
EMERGENCY PROCEDURES

When All Automated Systems Are Down:
1. Assess situation: Determine expected downtime
2. Contact immediate support: Notify Laboratory Managers and Laboratory Directors with Service Reference number
3. Prioritize samples: Process STAT and urgent samples first
4. Use manual methods: Consider sending to reference lab or backup analyzer
5. Document everything: Keep detailed records of all actions
6. Call for help: Contact service representatives and managers
7. Communicate delays: Inform requesting physicians of delays

Contamination Incidents:
1. Immediate containment: Isolate affected area
2. Personal protection: Ensure staff safety with PPE
3. Stop testing: Halt all operations in affected area
4. Clean and disinfect: Use appropriate disinfectants
5. Contact support: Notify Laboratory Managers and Laboratory Directors
6. Document incident: Complete incident report
7. Restart procedures: Only after thorough decontamination

Power Failure Response:
1. Secure samples: Ensure proper storage temperature
2. Document time: Record exact time of power failure
3. Check emergency power: Verify backup systems operational
4. Preserve reagents: Maintain cold chain if possible
5. Contact support: Notify Laboratory Managers and Laboratory Directors
6. Recovery planning: Prepare for system restart procedures
""",
            "downtime_procedures": """
IMPORTANT: Instrument Downtime or Issues Running Specimens
If the automated instruments are down or there are issues running a specimen, send to MOB lab or send to other regional laboratory with a working instrument. Use the alphabetical file to keep track of requisitions received.

LIS Downtime Operations
Error Message Management During LIS Downtime
Error messages on instruments when running patients during LIS downtime are acceptable because:
1. Expected behavior - The instruments are correctly detecting and reporting the loss of LIS connectivity
2. Operations can continue - Most modern laboratory instruments can operate in standalone mode
3. Results are preserved - Instruments store results locally in their internal memory during downtime
4. Downtime procedures activated - The error message serves as a clear indicator to follow downtime protocols
5. No actual malfunction - The error reflects a known, temporary communication issue
6. Recovery is straightforward - Once LIS connectivity is restored, stored results can be transmitted

High-Demand Laboratory Operations During Downtime
To maintain patient testing efficiency during LIS downtime:
* Continue testing on all instruments despite error messages
* Use manual logging to track all specimens tested
* Print instrument results immediately after testing
* Maintain chronological order of testing for proper recovery
* Communicate delays to requesting departments
* Prioritize STAT and urgent specimens
* Follow established downtime workflows to minimize disruption
""",
            "quality_assurance": """
QUALITY ASSURANCE

Documentation Requirements
QC Records Must Include:
* Date and time of QC run
* Operator identification
* Control lot numbers and expiration dates
* Results for all parameters
* Acceptable ranges
* Pass/Fail status
* Corrective actions taken
* Supervisor review and approval

Record Keeping Procedure and Protocol
⚠️ One Strike Policy for Documentation Mistakes:
Documentation errors are treated with utmost seriousness to maintain laboratory integrity and patient safety.

Usage of Proper Documentation Tools:
* Electronic Records: All entries must be made in approved LIS/EMR systems
* Corrections: Single line through error, initial, date, and reason for change
* No Erasures: Never use white-out, erasers, or delete electronic entries
* Contemporaneous: Document in real-time, never pre or post-date
* Complete Entries: All fields must be completed; use "N/A" if not applicable
* Audit Trail: All electronic changes tracked automatically

Competency Assessment:
Assessment Type    Frequency    Components
Initial           Upon hire    Direct observation, written test, problem solving
Annual           Yearly       Direct observation, QC review, proficiency testing
Remedial         As needed    Focused on identified deficiencies
""",
            "technical_support": """
TECHNICAL SUPPORT

Contact Guidelines by Issue Type:
* Technical questions: Lead Technologist, Technical Quality Specialist, and Laboratory Manager
* Equipment problems: Instrument Technical Support, Technical Quality Specialist, Biomedical Engineering and Laboratory Managers
* QC failures: Lead Technologist, Technical Quality Specialist, and Laboratory Manager
* Critical values: Ordering physician and nurses
* Result interpretation: Laboratory Manager and Laboratory Director
* After hours: On-call Laboratory Manager/Director
* IT issues: Laboratory Information Systems Support
* Supply issues: Laboratory Manager, Lead Technologist, Inventory Team and Technical Quality Specialist

Emergency Contact Hierarchy:
Immediate: Lead Technologist
If unavailable: Laboratory Manager
After hours: On-call Manager/Director
Document all communications in incident log
""",
            "regulatory_compliance": """
REGULATORY COMPLIANCE

CLIA Requirements:
* Certificate of Accreditation maintained
* Personnel meet qualification requirements
* Proficiency testing participation and passing scores
* Quality control performed as required
* Procedure manual available and followed
* Results reported within established TAT

CAP Standards:
* All CAP checklist requirements met
* Instrument maintenance documented
* Temperature logs maintained
* Reagent storage appropriate
* Safety requirements followed
* Quality management program active

OSHA Compliance:
* Bloodborne pathogen training current
* PPE available and used appropriately
* Exposure control plan in place
* Safety data sheets accessible
* Waste disposal procedures followed

Documentation Retention:
Document Type                    Retention Period
Patient results                  2 years minimum
Quality control records          2 years
Instrument maintenance          2 years
Personnel records               2 years post-employment
Proficiency testing             2 years
""",
            "references": """
REFERENCES

Laboratory Standard Operating Procedures 
Clinical and Laboratory Standards Institute (CLSI) Guidelines
Manufacturer Documentation
Regulatory and Accreditation Standards
Textbooks and Educational Resources
Online Resources

Note: All online resources should be accessed through secure connections. For internal resources, use VPN when accessing from outside the facility network.
"""
        }
    
    def generate_sop_template(self, test_name, instrument_name=None, department=None):
        """Generate a complete SOP template"""
        
        sop_content = f"""
# Standard Operating Procedure
## {test_name}
{f"**Instrument**: {instrument_name}" if instrument_name else ""}
{f"**Department**: {department}" if department else ""}

**Document Code**: LAB.SOP.{datetime.now().strftime('%Y%m%d')}
**Effective Date**: {datetime.now().strftime('%Y-%m-%d')}
**Version**: 1.0

---

"""
        
        for i, section in enumerate(self.sop_structure, 1):
            sop_content += f"\n## {i}. {section}\n\n"
            
            # Add standard content for specific sections
            if section == "MAINTENANCE":
                sop_content += "### Task Reference Guide\n"
                sop_content += "[Task-specific procedures will be documented here]\n\n"
                sop_content += "### QC Failure Actions\n"
                sop_content += self.standard_components["qc_failure_actions"]
                sop_content += "\n### Documentation Requirements\n"
                sop_content += self.standard_components["documentation_requirements"]
                
            elif section == "TEST PROCEDURE":
                sop_content += self.standard_components["critical_qc_rule"]
                sop_content += "\n### Turnaround Time Requirements\n"
                sop_content += self.standard_components["tat_requirements"]
                
            elif section == "EMERGENCY PROCEDURES":
                sop_content += self.standard_components["emergency_procedures"]
                
            elif section == "QUALITY ASSURANCE":
                sop_content += self.standard_components["quality_assurance"]
                
            elif section == "TECHNICAL SUPPORT":
                if instrument_name:
                    sop_content += f"{instrument_name} Technical Support:\n"
                    sop_content += "* Phone: [Insert phone number]\n"
                    sop_content += "* Hours: Monday-Friday, 8:00 AM - 5:00 PM EST\n"
                    sop_content += "* Email: [Insert email]\n"
                    sop_content += "* Website: [Insert website]\n\n"
                sop_content += self.standard_components["technical_support"]
                
            elif section == "REGULATORY COMPLIANCE":
                sop_content += self.standard_components["regulatory_compliance"]
                
            elif section == "DOWNTIME PROCEDURES":
                downtime_content = self.standard_components["downtime_procedures"]
                if instrument_name:
                    downtime_content = downtime_content.replace("automated instruments", f"automated {instrument_name} instruments")
                sop_content += downtime_content
                
            elif section == "REFERENCES":
                sop_content += self.standard_components["references"]
                
            else:
                sop_content += f"[Content for {section} section to be added]\n\n"
        
        return sop_content
    
    def create_sop_file(self, test_name, instrument_name=None, department=None, output_dir="./"):
        """Create a complete SOP file"""
        
        # Generate SOP content
        sop_content = self.generate_sop_template(test_name, instrument_name, department)
        
        # Create filename
        safe_name = test_name.replace(" ", "_").replace("/", "_")
        filename = f"SOP_{safe_name}_{datetime.now().strftime('%Y%m%d')}.md"
        filepath = Path(output_dir) / filename
        
        # Ensure output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Write SOP file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(sop_content)
        
        return filepath
    
    def create_html_sop(self, test_name, instrument_name=None, department=None, output_dir="./"):
        """Create an HTML version of the SOP"""
        
        # Generate markdown content
        md_content = self.generate_sop_template(test_name, instrument_name, department)
        
        # Convert to HTML format
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SOP - {test_name}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1, h2, h3 {{
            color: #2c3e50;
        }}
        h1 {{
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            border-bottom: 2px solid #bdc3c7;
            padding-bottom: 8px;
            margin-top: 30px;
        }}
        h3 {{
            color: #34495e;
            margin-top: 25px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
        }}
        th, td {{
            border: 1px solid #bdc3c7;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #ecf0f1;
            font-weight: bold;
        }}
        .warning {{
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 15px;
            margin: 15px 0;
        }}
        .critical {{
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 5px;
            padding: 15px;
            margin: 15px 0;
        }}
        ul, ol {{
            margin: 10px 0;
            padding-left: 30px;
        }}
        li {{
            margin: 5px 0;
        }}
        .header-info {{
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 30px;
        }}
        .section-number {{
            color: #3498db;
            font-weight: bold;
        }}
        @media print {{
            body {{
                margin: 0;
                padding: 15px;
            }}
            .no-print {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
"""
        
        # Process markdown to HTML
        lines = md_content.split('\n')
        in_table = False
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('# '):
                html_content += f'<h1>{line[2:]}</h1>\n'
            elif line.startswith('## '):
                if line[3:].split('.')[0].isdigit():
                    section_num = line[3:].split('.')[0]
                    section_title = '.'.join(line[3:].split('.')[1:]).strip()
                    html_content += f'<h2><span class="section-number">{section_num}.</span> {section_title}</h2>\n'
                else:
                    html_content += f'<h2>{line[3:]}</h2>\n'
            elif line.startswith('### '):
                html_content += f'<h3>{line[4:]}</h3>\n'
            elif line.startswith('**') and line.endswith('**'):
                html_content += f'<div class="header-info"><strong>{line[2:-2]}</strong></div>\n'
            elif line.startswith('⚠️'):
                html_content += f'<div class="warning">{line}</div>\n'
            elif line.startswith('* '):
                html_content += f'<ul><li>{line[2:]}</li></ul>\n'
            elif line.startswith('- '):
                html_content += f'<ul><li>{line[2:]}</li></ul>\n'
            elif '|' in line and not in_table:
                # Start of table
                in_table = True
                html_content += '<table>\n'
                headers = [cell.strip() for cell in line.split('|')[1:-1]]
                html_content += '<tr>\n'
                for header in headers:
                    html_content += f'<th>{header}</th>\n'
                html_content += '</tr>\n'
            elif '|' in line and in_table:
                if '---' in line:
                    continue  # Skip separator row
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                html_content += '<tr>\n'
                for cell in cells:
                    html_content += f'<td>{cell}</td>\n'
                html_content += '</tr>\n'
            elif line == '' and in_table:
                in_table = False
                html_content += '</table>\n'
            elif line:
                html_content += f'<p>{line}</p>\n'
            else:
                html_content += '<br>\n'
        
        html_content += """
</body>
</html>
"""
        
        # Create filename
        safe_name = test_name.replace(" ", "_").replace("/", "_")
        filename = f"SOP_{safe_name}_{datetime.now().strftime('%Y%m%d')}.html"
        filepath = Path(output_dir) / filename
        
        # Ensure output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Write HTML file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath

def main():
    """Main function for SOP generation"""
    
    print("🏥 Laboratory Standard Operating Procedure Generator")
    print("=" * 60)
    
    generator = SOPGenerator()
    
    # Example SOPs to generate
    example_sops = [
        {
            "test_name": "Complete Blood Count (CBC)",
            "instrument_name": "Sysmex XN-Series",
            "department": "Hematology"
        },
        {
            "test_name": "Basic Metabolic Panel (BMP)",
            "instrument_name": "Abbott Architect c4000",
            "department": "Chemistry"
        },
        {
            "test_name": "Prothrombin Time (PT/INR)",
            "instrument_name": "Stago Compact Max",
            "department": "Coagulation"
        },
        {
            "test_name": "Urinalysis Complete",
            "instrument_name": "Siemens Clinitek Novus",
            "department": "Urinalysis"
        }
    ]
    
    output_dir = "/Users/ugochi141/Desktop/SOP 2025"
    
    print(f"📂 Output Directory: {output_dir}")
    print("🔧 Generating Standard Operating Procedures...")
    print()
    
    for sop_info in example_sops:
        print(f"Creating SOP for {sop_info['test_name']}...")
        
        # Create both markdown and HTML versions
        md_file = generator.create_sop_file(
            sop_info['test_name'],
            sop_info['instrument_name'], 
            sop_info['department'],
            output_dir
        )
        
        html_file = generator.create_html_sop(
            sop_info['test_name'],
            sop_info['instrument_name'],
            sop_info['department'], 
            output_dir
        )
        
        print(f"  ✅ Markdown: {md_file}")
        print(f"  ✅ HTML: {html_file}")
        print()
    
    print("🎉 SOP Generation Complete!")
    print()
    print("📋 Generated SOPs include all standard sections:")
    for i, section in enumerate(generator.sop_structure, 1):
        print(f"  {i}. {section}")
    
    print("\n📚 All SOPs include:")
    print("  • Comprehensive documentation requirements")
    print("  • Quality control procedures and failure actions")
    print("  • Emergency and downtime procedures")
    print("  • Regulatory compliance information")
    print("  • Technical support contacts")
    print("  • Standardized formatting and structure")
    
    return 0

if __name__ == "__main__":
    exit(main())