#!/usr/bin/env python3
"""
SOP Customization Tool
Customizes standard SOPs for specific instruments and laboratory tests
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime

class SOPCustomizer:
    """Customize SOPs for specific laboratory instruments and tests"""
    
    def __init__(self):
        self.instrument_configs = {
            "sysmex_xn": {
                "name": "Sysmex XN-Series",
                "manufacturer": "Sysmex Corporation",
                "support_phone": "1-800-935-3595",
                "support_email": "support@sysmex.com",
                "support_hours": "Monday-Friday, 8:00 AM - 5:00 PM EST",
                "downtime_replacement": "Sysmex XN instruments",
                "backup_method": "Manual differential count or send to reference lab"
            },
            "stago_compact": {
                "name": "Stago Compact Max",
                "manufacturer": "Stago Diagnostics",
                "support_phone": "1-800-222-3260", 
                "support_email": "technical.support@stago-us.com",
                "support_hours": "Monday-Friday, 8:00 AM - 5:00 PM EST",
                "downtime_replacement": "Stago Compact Max instruments",
                "backup_method": "Manual coagulation methods or send to reference lab"
            },
            "abbott_architect": {
                "name": "Abbott Architect c4000/c8000",
                "manufacturer": "Abbott Diagnostics",
                "support_phone": "1-800-553-7042",
                "support_email": "technical.support@abbott.com", 
                "support_hours": "24/7 technical support available",
                "downtime_replacement": "Abbott Architect instruments",
                "backup_method": "Alternative chemistry analyzer or send to reference lab"
            },
            "siemens_clinitek": {
                "name": "Siemens Clinitek Novus",
                "manufacturer": "Siemens Healthineers",
                "support_phone": "1-888-826-9702",
                "support_email": "customer.care@siemens-healthineers.com",
                "support_hours": "Monday-Friday, 8:00 AM - 6:00 PM EST",
                "downtime_replacement": "Siemens Clinitek instruments", 
                "backup_method": "Manual urinalysis with microscopy"
            }
        }
        
        self.test_configs = {
            "cbc": {
                "name": "Complete Blood Count",
                "tat_stat": "60 minutes",
                "tat_routine": "4 hours", 
                "critical_values": ["WBC <1.0 or >50.0", "Hgb <5.0 or >20.0", "Plt <20 or >1000"],
                "specimen": "EDTA whole blood (lavender top)",
                "stability": "24 hours at room temperature",
                "reference_ranges": {
                    "WBC": "4.0-11.0 x10³/μL",
                    "RBC": "4.2-5.4 x10⁶/μL (M), 3.6-5.0 x10⁶/μL (F)",
                    "Hgb": "14.0-18.0 g/dL (M), 12.0-16.0 g/dL (F)",
                    "Hct": "42-52% (M), 37-47% (F)",
                    "Platelet": "150-400 x10³/μL"
                }
            },
            "bmp": {
                "name": "Basic Metabolic Panel",
                "tat_stat": "60 minutes",
                "tat_routine": "4 hours",
                "critical_values": ["Glucose <40 or >500", "Potassium <2.5 or >6.0", "Sodium <120 or >160"],
                "specimen": "Serum or plasma (SST or green top)",
                "stability": "7 days refrigerated",
                "reference_ranges": {
                    "Glucose": "70-99 mg/dL (fasting)",
                    "BUN": "7-20 mg/dL", 
                    "Creatinine": "0.7-1.3 mg/dL (M), 0.6-1.1 mg/dL (F)",
                    "Sodium": "136-145 mmol/L",
                    "Potassium": "3.5-5.1 mmol/L",
                    "Chloride": "98-107 mmol/L",
                    "CO2": "22-29 mmol/L"
                }
            },
            "pt_inr": {
                "name": "Prothrombin Time/INR",
                "tat_stat": "60 minutes", 
                "tat_routine": "2 hours",
                "critical_values": ["INR >5.0", "PT >50 seconds"],
                "specimen": "Citrated plasma (blue top)",
                "stability": "4 hours at room temperature, 24 hours refrigerated",
                "reference_ranges": {
                    "PT": "11.0-13.0 seconds",
                    "INR": "0.8-1.2 (not on anticoagulation)"
                }
            },
            "urinalysis": {
                "name": "Urinalysis Complete",
                "tat_stat": "60 minutes",
                "tat_routine": "4 hours", 
                "critical_values": ["Positive nitrites", "Large blood", "Many bacteria"],
                "specimen": "Random urine (sterile container)",
                "stability": "2 hours at room temperature, 24 hours refrigerated",
                "reference_ranges": {
                    "Color": "Yellow to amber",
                    "Clarity": "Clear to slightly hazy",
                    "Specific Gravity": "1.003-1.030",
                    "pH": "5.0-8.0",
                    "Protein": "Negative to trace",
                    "Glucose": "Negative",
                    "Blood": "Negative",
                    "Nitrites": "Negative"
                }
            }
        }
    
    def customize_sop(self, test_type, instrument_type, output_file):
        """Customize an SOP for specific test and instrument"""
        
        if test_type not in self.test_configs:
            print(f"❌ Test type '{test_type}' not found in configurations")
            return False
            
        if instrument_type not in self.instrument_configs:
            print(f"❌ Instrument type '{instrument_type}' not found in configurations")
            return False
        
        test_config = self.test_configs[test_type]
        instrument_config = self.instrument_configs[instrument_type]
        
        # Generate customized SOP content
        sop_content = self.generate_customized_sop(test_config, instrument_config)
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(sop_content)
        
        print(f"✅ Customized SOP created: {output_file}")
        return True
    
    def generate_customized_sop(self, test_config, instrument_config):
        """Generate fully customized SOP content"""
        
        sop_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SOP - {test_config['name']} - {instrument_config['name']}</title>
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
        .header-box {{
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 20px;
            margin-bottom: 30px;
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
        ul, ol {{
            margin: 10px 0;
            padding-left: 30px;
        }}
        li {{
            margin: 5px 0;
        }}
        .section-number {{
            color: #3498db;
            font-weight: bold;
        }}
    </style>
</head>
<body>

<h1>Standard Operating Procedure</h1>
<h2>{test_config['name']} - {instrument_config['name']}</h2>

<div class="header-box">
    <table>
        <tr>
            <td><strong>Test Name:</strong></td>
            <td>{test_config['name']}</td>
            <td><strong>Instrument:</strong></td>
            <td>{instrument_config['name']}</td>
        </tr>
        <tr>
            <td><strong>Manufacturer:</strong></td>
            <td>{instrument_config['manufacturer']}</td>
            <td><strong>Document Code:</strong></td>
            <td>LAB.SOP.{datetime.now().strftime('%Y%m%d')}</td>
        </tr>
        <tr>
            <td><strong>Effective Date:</strong></td>
            <td>{datetime.now().strftime('%Y-%m-%d')}</td>
            <td><strong>Version:</strong></td>
            <td>1.0</td>
        </tr>
    </table>
</div>

<h2><span class="section-number">1.</span> PURPOSE</h2>
<p>This SOP provides standardized procedures for performing {test_config['name']} testing using the {instrument_config['name']} analyzer to ensure accurate, reliable, and timely results for patient care.</p>

<h2><span class="section-number">2.</span> CLINICAL SIGNIFICANCE</h2>
<p>The {test_config['name']} provides essential diagnostic information for:</p>
<ul>
    <li>Patient diagnosis and monitoring</li>
    <li>Treatment decisions and therapy monitoring</li>
    <li>Disease screening and prevention</li>
    <li>Emergency and critical care assessment</li>
</ul>

<h2><span class="section-number">3.</span> SCOPE</h2>
<p>This procedure applies to all laboratory personnel performing {test_config['name']} testing on the {instrument_config['name']} in the clinical laboratory. It covers specimen handling, instrument operation, quality control, result reporting, and troubleshooting.</p>

<h2><span class="section-number">4.</span> RESPONSIBILITIES</h2>
<ul>
    <li><strong>Laboratory Technologists:</strong> Perform testing, quality control, and result verification</li>
    <li><strong>Lead Technologist:</strong> Training, competency assessment, and procedure oversight</li>
    <li><strong>Technical Quality Specialist:</strong> SOP maintenance, quality assurance, and regulatory compliance</li>
    <li><strong>Laboratory Manager:</strong> Resource allocation, staff supervision, and operational oversight</li>
    <li><strong>Laboratory Director:</strong> Medical oversight, result interpretation, and clinical correlation</li>
</ul>

<h2><span class="section-number">5.</span> SAFETY REQUIREMENTS</h2>
<ul>
    <li>Follow Universal Precautions for all specimens</li>
    <li>Wear appropriate PPE: gloves, lab coat, safety glasses</li>
    <li>Handle all specimens as potentially infectious</li>
    <li>Dispose of biohazardous waste according to facility procedures</li>
    <li>Report all accidents and exposures immediately</li>
    <li>Maintain current training on bloodborne pathogen safety</li>
</ul>

<h2><span class="section-number">6.</span> SPECIMEN REQUIREMENTS</h2>
<table>
    <tr>
        <th>Parameter</th>
        <th>Requirement</th>
    </tr>
    <tr>
        <td>Specimen Type</td>
        <td>{test_config['specimen']}</td>
    </tr>
    <tr>
        <td>Minimum Volume</td>
        <td>As per instrument requirements</td>
    </tr>
    <tr>
        <td>Stability</td>
        <td>{test_config['stability']}</td>
    </tr>
    <tr>
        <td>Storage</td>
        <td>Room temperature or refrigerated as appropriate</td>
    </tr>
    <tr>
        <td>Rejection Criteria</td>
        <td>Hemolyzed, clotted, insufficient volume, unlabeled</td>
    </tr>
</table>

<h2><span class="section-number">7.</span> REAGENTS AND SUPPLIES</h2>
<p>Use only reagents and supplies approved for use with the {instrument_config['name']}:</p>
<ul>
    <li>Manufacturer-approved reagents and controls</li>
    <li>Calibration materials as specified</li>
    <li>Quality control materials</li>
    <li>Consumables (tips, cuvettes, etc.)</li>
    <li>Cleaning and maintenance supplies</li>
</ul>

<h2><span class="section-number">8.</span> EQUIPMENT</h2>
<ul>
    <li><strong>Primary Analyzer:</strong> {instrument_config['name']}</li>
    <li>Computer system with laboratory information system (LIS) connection</li>
    <li>Backup power supply (UPS)</li>
    <li>Temperature monitoring equipment</li>
    <li>Refrigeration units for reagent storage</li>
    <li>Centrifuge (if required for specimen preparation)</li>
</ul>

<h2><span class="section-number">9.</span> MAINTENANCE</h2>

<h3>Task Reference Guide</h3>
<p>Daily, weekly, monthly, and quarterly maintenance tasks are documented in the instrument manual and maintenance log. All maintenance must be performed by trained personnel and documented appropriately.</p>

<h3>QC Failure Actions</h3>
<div class="critical">
<strong>QC Failure Actions:</strong>
<ol>
    <li>Repeat QC analysis</li>
    <li>Check reagent expiration dates</li>
    <li>Inspect instrument for problems</li>
    <li>Contact manager if QC continues to fail</li>
    <li><strong>Do NOT report patient results until QC is acceptable</strong></li>
</ol>
</div>

<h3>Documentation Requirements</h3>
<table>
    <tr>
        <th>Document Type</th>
        <th>Retention Period</th>
    </tr>
    <tr>
        <td>Patient results</td>
        <td>2 years minimum</td>
    </tr>
    <tr>
        <td>Quality control records</td>
        <td>2 years</td>
    </tr>
    <tr>
        <td>Instrument maintenance</td>
        <td>2 years</td>
    </tr>
    <tr>
        <td>Personnel records</td>
        <td>2 years post-employment</td>
    </tr>
    <tr>
        <td>Proficiency testing</td>
        <td>2 years</td>
    </tr>
</table>

<h2><span class="section-number">10.</span> QUALITY CONTROL REQUIREMENTS</h2>
<ul>
    <li>Run QC materials at the beginning of each shift</li>
    <li>Run QC with each new reagent lot</li>
    <li>Document all QC results</li>
    <li>Investigate all out-of-control results</li>
    <li>Do not report patient results if QC is unacceptable</li>
</ul>

<h2><span class="section-number">11.</span> CALIBRATION</h2>
<p>Calibration procedures must follow manufacturer specifications and laboratory policies. Calibration frequency and acceptance criteria are documented in the instrument manual.</p>

<h2><span class="section-number">12.</span> TROUBLESHOOTING</h2>
<p>Common troubleshooting procedures are documented in the instrument manual. For persistent problems, contact technical support immediately and document all troubleshooting steps.</p>

<h2><span class="section-number">13.</span> TEST PROCEDURE</h2>

<div class="critical">
<strong>⚠️ Critical QC Rule:</strong><br>
NEVER report patient results if QC is not acceptable. Patient safety depends on accurate results. If QC fails, troubleshoot and repeat. If still failing, use backup method or send to reference lab.

<p><strong>Follow-up Notification Requirements:</strong></p>
<ol>
    <li>Immediately notify Lead Technologist of QC failure</li>
    <li>Document all troubleshooting steps attempted</li>
    <li>Contact {instrument_config['name']} Tech Support and obtain reference number</li>
    <li>Notify Technical Quality Specialist with:
        <ul>
            <li>All troubleshooting steps performed</li>
            <li>Tech support reference number</li>
            <li>Current instrument status</li>
        </ul>
    </li>
    <li>Notify Laboratory Manager with complete documentation</li>
</ol>
<p><strong>CRITICAL:</strong> Before contacting Technical Quality Specialist and Lab Manager, ensure you have documented all troubleshooting steps and obtained the reference number from Tech Support.</p>
</div>

<h3>Turnaround Time Requirements</h3>
<table>
    <tr>
        <th>Priority</th>
        <th>TAT Goal</th>
        <th>Measured From</th>
        <th>Compliance Target</th>
    </tr>
    <tr>
        <td>STAT</td>
        <td>{test_config['tat_stat']}</td>
        <td>Receipt in lab to result</td>
        <td>≥90%</td>
    </tr>
    <tr>
        <td>Routine</td>
        <td>{test_config['tat_routine']}</td>
        <td>Receipt in lab to result</td>
        <td>≥85%</td>
    </tr>
    <tr>
        <td>Critical Values</td>
        <td>30 minutes</td>
        <td>Result verification to notification</td>
        <td>100%</td>
    </tr>
</table>

<h2><span class="section-number">14.</span> CALCULATIONS AND RESULT REPORTING</h2>
<p>Results are calculated automatically by the {instrument_config['name']} and transmitted to the LIS. All results must be reviewed and verified before release.</p>

<h2><span class="section-number">15.</span> REFERENCE RANGES</h2>
<table>
    <tr>
        <th>Parameter</th>
        <th>Reference Range</th>
    </tr>"""
        
        for param, range_val in test_config['reference_ranges'].items():
            sop_content += f"""
    <tr>
        <td>{param}</td>
        <td>{range_val}</td>
    </tr>"""
        
        sop_content += f"""
</table>

<h2><span class="section-number">16.</span> CRITICAL VALUES</h2>
<p><strong>Critical values requiring immediate notification:</strong></p>
<ul>"""
        
        for critical_value in test_config['critical_values']:
            sop_content += f"<li>{critical_value}</li>"
        
        sop_content += f"""
</ul>
<p>All critical values must be called to the ordering physician within 30 minutes of result verification.</p>

<h2><span class="section-number">17.</span> LIMITATIONS AND INTERFERENCES</h2>
<p>Refer to manufacturer's package insert for detailed information on test limitations, interferences, and precautions specific to the {instrument_config['name']}.</p>

<h2><span class="section-number">18.</span> EMERGENCY PROCEDURES</h2>

<h3>When All Automated Systems Are Down:</h3>
<ol>
    <li>Assess situation: Determine expected downtime</li>
    <li>Contact immediate support: Notify Laboratory Managers and Laboratory Directors with Service Reference number</li>
    <li>Prioritize samples: Process STAT and urgent samples first</li>
    <li>Use manual methods: {instrument_config['backup_method']}</li>
    <li>Document everything: Keep detailed records of all actions</li>
    <li>Call for help: Contact service representatives and managers</li>
    <li>Communicate delays: Inform requesting physicians of delays</li>
</ol>

<h3>Contamination Incidents:</h3>
<ol>
    <li>Immediate containment: Isolate affected area</li>
    <li>Personal protection: Ensure staff safety with PPE</li>
    <li>Stop testing: Halt all operations in affected area</li>
    <li>Clean and disinfect: Use appropriate disinfectants</li>
    <li>Contact support: Notify Laboratory Managers and Laboratory Directors</li>
    <li>Document incident: Complete incident report</li>
    <li>Restart procedures: Only after thorough decontamination</li>
</ol>

<h2><span class="section-number">19.</span> TECHNICAL SUPPORT</h2>

<h3>{instrument_config['name']} Technical Support:</h3>
<table>
    <tr>
        <th>Contact Method</th>
        <th>Information</th>
    </tr>
    <tr>
        <td>Phone</td>
        <td>{instrument_config['support_phone']}</td>
    </tr>
    <tr>
        <td>Email</td>
        <td>{instrument_config['support_email']}</td>
    </tr>
    <tr>
        <td>Hours</td>
        <td>{instrument_config['support_hours']}</td>
    </tr>
</table>

<h3>Contact Guidelines by Issue Type:</h3>
<ul>
    <li><strong>Technical questions:</strong> Lead Technologist, Technical Quality Specialist, and Laboratory Manager</li>
    <li><strong>Equipment problems:</strong> Instrument Technical Support, Technical Quality Specialist, Biomedical Engineering and Laboratory Managers</li>
    <li><strong>QC failures:</strong> Lead Technologist, Technical Quality Specialist, and Laboratory Manager</li>
    <li><strong>Critical values:</strong> Ordering physician and nurses</li>
    <li><strong>Result interpretation:</strong> Laboratory Manager and Laboratory Director</li>
    <li><strong>After hours:</strong> On-call Laboratory Manager/Director</li>
    <li><strong>IT issues:</strong> Laboratory Information Systems Support</li>
    <li><strong>Supply issues:</strong> Laboratory Manager, Lead Technologist, Inventory Team and Technical Quality Specialist</li>
</ul>

<p><strong>Emergency Contact Hierarchy:</strong></p>
<ol>
    <li>Immediate: Lead Technologist</li>
    <li>If unavailable: Laboratory Manager</li>
    <li>After hours: On-call Manager/Director</li>
</ol>
<p><em>Document all communications in incident log</em></p>

<h2><span class="section-number">20.</span> QUALITY ASSURANCE</h2>

<h3>Documentation Requirements</h3>
<p><strong>QC Records Must Include:</strong></p>
<ul>
    <li>Date and time of QC run</li>
    <li>Operator identification</li>
    <li>Control lot numbers and expiration dates</li>
    <li>Results for all parameters</li>
    <li>Acceptable ranges</li>
    <li>Pass/Fail status</li>
    <li>Corrective actions taken</li>
    <li>Supervisor review and approval</li>
</ul>

<div class="warning">
<strong>⚠️ One Strike Policy for Documentation Mistakes:</strong><br>
Documentation errors are treated with utmost seriousness to maintain laboratory integrity and patient safety.

<p><strong>Usage of Proper Documentation Tools:</strong></p>
<ul>
    <li><strong>Electronic Records:</strong> All entries must be made in approved LIS/EMR systems</li>
    <li><strong>Corrections:</strong> Single line through error, initial, date, and reason for change</li>
    <li><strong>No Erasures:</strong> Never use white-out, erasers, or delete electronic entries</li>
    <li><strong>Contemporaneous:</strong> Document in real-time, never pre or post-date</li>
    <li><strong>Complete Entries:</strong> All fields must be completed; use "N/A" if not applicable</li>
    <li><strong>Audit Trail:</strong> All electronic changes tracked automatically</li>
</ul>
</div>

<h3>Competency Assessment</h3>
<table>
    <tr>
        <th>Assessment Type</th>
        <th>Frequency</th>
        <th>Components</th>
    </tr>
    <tr>
        <td>Initial</td>
        <td>Upon hire</td>
        <td>Direct observation, written test, problem solving</td>
    </tr>
    <tr>
        <td>Annual</td>
        <td>Yearly</td>
        <td>Direct observation, QC review, proficiency testing</td>
    </tr>
    <tr>
        <td>Remedial</td>
        <td>As needed</td>
        <td>Focused on identified deficiencies</td>
    </tr>
</table>

<h2><span class="section-number">21.</span> REGULATORY COMPLIANCE</h2>

<h3>CLIA Requirements:</h3>
<ul>
    <li>Certificate of Accreditation maintained</li>
    <li>Personnel meet qualification requirements</li>
    <li>Proficiency testing participation and passing scores</li>
    <li>Quality control performed as required</li>
    <li>Procedure manual available and followed</li>
    <li>Results reported within established TAT</li>
</ul>

<h3>CAP Standards:</h3>
<ul>
    <li>All CAP checklist requirements met</li>
    <li>Instrument maintenance documented</li>
    <li>Temperature logs maintained</li>
    <li>Reagent storage appropriate</li>
    <li>Safety requirements followed</li>
    <li>Quality management program active</li>
</ul>

<h3>OSHA Compliance:</h3>
<ul>
    <li>Bloodborne pathogen training current</li>
    <li>PPE available and used appropriately</li>
    <li>Exposure control plan in place</li>
    <li>Safety data sheets accessible</li>
    <li>Waste disposal procedures followed</li>
</ul>

<h2><span class="section-number">22.</span> DOWNTIME PROCEDURES</h2>

<div class="warning">
<strong>IMPORTANT: Instrument Downtime or Issues Running Specimens</strong><br>
If the automated {instrument_config['downtime_replacement']} are down or there are issues running a specimen, send to MOB lab or send to other regional laboratory with a working instrument. Use the alphabetical file to keep track of requisitions received.
</div>

<h3>LIS Downtime Operations</h3>
<p><strong>Error Message Management During LIS Downtime</strong></p>
<p>Error messages on instruments when running patients during LIS downtime are acceptable because:</p>
<ol>
    <li><strong>Expected behavior</strong> - The instruments are correctly detecting and reporting the loss of LIS connectivity</li>
    <li><strong>Operations can continue</strong> - Most modern laboratory instruments can operate in standalone mode</li>
    <li><strong>Results are preserved</strong> - Instruments store results locally in their internal memory during downtime</li>
    <li><strong>Downtime procedures activated</strong> - The error message serves as a clear indicator to follow downtime protocols</li>
    <li><strong>No actual malfunction</strong> - The error reflects a known, temporary communication issue</li>
    <li><strong>Recovery is straightforward</strong> - Once LIS connectivity is restored, stored results can be transmitted</li>
</ol>

<h3>High-Demand Laboratory Operations During Downtime</h3>
<p>To maintain patient testing efficiency during LIS downtime:</p>
<ul>
    <li>Continue testing on all instruments despite error messages</li>
    <li>Use manual logging to track all specimens tested</li>
    <li>Print instrument results immediately after testing</li>
    <li>Maintain chronological order of testing for proper recovery</li>
    <li>Communicate delays to requesting departments</li>
    <li>Prioritize STAT and urgent specimens</li>
    <li>Follow established downtime workflows to minimize disruption</li>
</ul>

<h2><span class="section-number">23.</span> REFERENCES</h2>
<ul>
    <li>Laboratory Standard Operating Procedures</li>
    <li>Clinical and Laboratory Standards Institute (CLSI) Guidelines</li>
    <li>{instrument_config['name']} Operator Manual</li>
    <li>{instrument_config['manufacturer']} Technical Documentation</li>
    <li>Regulatory and Accreditation Standards</li>
    <li>Textbooks and Educational Resources</li>
    <li>Online Resources</li>
</ul>

<p><em>Note: All online resources should be accessed through secure connections. For internal resources, use VPN when accessing from outside the facility network.</em></p>

<hr>
<p><em>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>

</body>
</html>
"""
        
        return sop_content

def main():
    """Main function for SOP customization"""
    
    parser = argparse.ArgumentParser(description='Customize laboratory SOPs for specific instruments and tests')
    parser.add_argument('--test', required=True, choices=['cbc', 'bmp', 'pt_inr', 'urinalysis'], 
                       help='Test type to customize')
    parser.add_argument('--instrument', required=True, 
                       choices=['sysmex_xn', 'stago_compact', 'abbott_architect', 'siemens_clinitek'],
                       help='Instrument type to customize for')
    parser.add_argument('--output', required=True, help='Output file path')
    
    args = parser.parse_args()
    
    customizer = SOPCustomizer()
    success = customizer.customize_sop(args.test, args.instrument, args.output)
    
    if success:
        print(f"\n🎉 Customized SOP created successfully!")
        print(f"📄 File: {args.output}")
        print(f"🧪 Test: {customizer.test_configs[args.test]['name']}")
        print(f"🔬 Instrument: {customizer.instrument_configs[args.instrument]['name']}")
        print(f"\n✅ SOP includes all required sections and customized content")
        return 0
    else:
        print(f"\n❌ Failed to create customized SOP")
        return 1

if __name__ == "__main__":
    exit(main())