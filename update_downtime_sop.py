#!/usr/bin/env python3
"""
Script to intelligently update the Downtime Procedures SOP with new content and images.
"""

import re
import base64
import os

# File paths
SOP_FILE = "/Users/ugochi141/Desktop/Largo Lab SOP 2025 Enhanced/untitled folder/Downtime_Procedures_SOP_FINAL_Kaiser_Integrated_BACKUP.html"
IMAGE_DIR = "/Users/ugochi141/Desktop/100125 Downtime Form"
OUTPUT_FILE = "/Users/ugochi141/Desktop/Largo Lab SOP 2025 Enhanced/untitled folder/Downtime_Procedures_SOP_FINAL_Kaiser_Integrated_UPDATED.html"

def read_image_as_base64(image_path):
    """Convert image to base64 data URI."""
    with open(image_path, 'rb') as f:
        b64_data = base64.b64encode(f.read()).decode('utf-8')
    return f"data:image/jpeg;base64,{b64_data}"

def create_specimens_without_requisition_section():
    """Create the section for specimens without requisition."""
    return '''
<div class="warning-box">
<h3>Specimens Received Without Requisition Slip</h3>
<p><strong>Applicable for:</strong></p>
<ul>
<li>All anatomic pathology specimens</li>
<li>All clinical lab specimens during downtime</li>
</ul>

<h4>Procedure for Handling Specimens Without Requisition:</h4>
<ol>
<li><strong>Do NOT reject irretrievable specimens</strong> (CSF, pleural fluid, peritoneal fluid, synovial fluid, pericardial fluid)</li>
<li><strong>Contact the ordering provider or nurse</strong> to obtain test orders and patient demographics</li>
<li><strong>Document all information</strong> on a downtime requisition form</li>
<li><strong>Assign a downtime accession number</strong> (DT-MMDD-###)</li>
<li><strong>Log the specimen</strong> in the downtime tracking log</li>
<li><strong>Process according to priority</strong> (STAT vs routine)</li>
<li><strong>When LIS is restored</strong>:
    <ul>
    <li>Manually enter the order in Cerner using Department Order Entry</li>
    <li>Verify patient demographics (name, DOB, MRN)</li>
    <li>Add encounter if needed</li>
    <li>Enter all tests from the downtime requisition</li>
    <li>Print labels and affix to specimens</li>
    <li>Log specimen with actual collection/receive time</li>
    <li>Result tests from instrument printouts</li>
    </ul>
</li>
<li><strong>Document in SIRI</strong> if any issues occurred</li>
</ol>

<div class="info-box">
<p><strong>Note:</strong> If the provider insists a specimen must be tested despite laboratory objections, refer the provider to the Laboratory Director and hold the sample until instructions are received.</p>
</div>
</div>
'''

def create_cerner_recovery_section(images_b64):
    """Create the Cerner Downtime Recovery section with images."""
    return f'''
<!-- CERNER DOWNTIME RECOVERY PROCEDURES -->
<div class="section" id="cerner-recovery">
<h2>8A. CERNER DOWNTIME RECOVERY PROCEDURES</h2>

<div class="key-concept">
<h3>Overview</h3>
<p>Once the LIS system is restored, the following steps reconcile orders and results in the Cerner Lab system. This document outlines two scenarios:</p>
<ul>
<li><strong>Part A:</strong> Orders NOT in Cerner (must be entered manually)</li>
<li><strong>Part B:</strong> Orders already present in Cerner (collection and resulting only)</li>
</ul>
</div>

<div class="procedure-section">
<h3>Part A: Order Not In Cerner</h3>
<p>If orders on your Lab Request Form are not in Cerner, proceed by entering the orders into Cerner:</p>

<ol>
<li><strong>Launch Department Order Entry</strong> from your App Bar.</li>

<li><strong>Search for Patient</strong>
    <ul>
    <li>Using Patient Registration (Red Book), pull up your patient</li>
    <li>Verify name, DOB, and MRN matches the Lab Request form</li>
    </ul>
</li>

<div style="text-align: center; margin: 20px 0;">
<img src="{images_b64['patient_search']}" style="max-width: 100%; border: 2px solid #0066cc; border-radius: 6px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);" alt="Patient Search Screen">
<p style="font-size: 9pt; color: #666; margin-top: 8px;"><em>Figure 1: Patient Search - Verify demographics match Lab Request Form</em></p>
</div>

<li><strong>Add Encounter</strong> for this patient if the encounter doesn't exist
    <ul>
    <li>Be sure to select the correct provider for the encounter</li>
    </ul>
</li>

<li><strong>Enter the Orders</strong> as listed on the Lab Request Form
    <ul>
    <li>Ensure the ordering provider is correct</li>
    <li>Complete all relevant fields (ICD 10 code, etc.)</li>
    <li><strong>Add Orders to Scratchpad</strong> until all orders have been added correctly</li>
    </ul>
</li>

<div style="text-align: center; margin: 20px 0;">
<img src="{images_b64['add_orders']}" style="max-width: 100%; border: 2px solid #0066cc; border-radius: 6px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);" alt="Add Orders to Scratchpad">
<p style="font-size: 9pt; color: #666; margin-top: 8px;"><em>Figure 2: Department Order Entry - Add orders to scratchpad</em></p>
</div>

<li><strong>Submit Orders</strong> when all orders are entered correctly
    <ul>
    <li>Hit the <strong>Submit Orders</strong> button</li>
    <li>Verify all orders were accepted by the system</li>
    </ul>
</li>

<div style="text-align: center; margin: 20px 0;">
<img src="{images_b64['submit_orders']}" style="max-width: 100%; border: 2px solid #0066cc; border-radius: 6px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);" alt="Submit Orders">
<p style="font-size: 9pt; color: #666; margin-top: 8px;"><em>Figure 3: Submit Orders button in Department Order Entry</em></p>
</div>

<li><strong>Proceed to Part B, Step 1</strong> to collect and result the specimen</li>
</ol>
</div>

<div class="procedure-section">
<h3>Part B: Orders in Cerner</h3>
<p>If the orders from your Lab Request Form are already in Cerner, proceed with the following steps:</p>

<ol>
<li><strong>Collect the Sample</strong>
    <ul>
    <li>Launch <strong>Collection Inquiry</strong> from the App Bar</li>
    <li>Search for the patient</li>
    <li>Select the tests that were completed during downtime</li>
    <li>Print labels at this point to attach to your instrument printouts</li>
    </ul>
</li>

<div style="text-align: center; margin: 20px 0;">
<img src="{images_b64['collection_inquiry']}" style="max-width: 100%; border: 2px solid #0066cc; border-radius: 6px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);" alt="Collection Inquiry">
<p style="font-size: 9pt; color: #666; margin-top: 8px;"><em>Figure 4: Collection Inquiry - Select completed tests</em></p>
</div>

<li><strong>Receive the Specimen</strong>
    <ul>
    <li>Launch <strong>Specimen Log-in</strong> from the App Bar</li>
    <li>Search for the patient using the accession number or MRN</li>
    <li>Correct the collection and receipt details to reflect actual times from Lab Request Form/downtime documents</li>
    <li>Log in the specimen</li>
    </ul>
</li>

<div style="text-align: center; margin: 20px 0;">
<img src="{images_b64['specimen_login']}" style="max-width: 100%; border: 2px solid #0066cc; border-radius: 6px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);" alt="Specimen Log-in">
<p style="font-size: 9pt; color: #666; margin-top: 8px;"><em>Figure 5: Specimen Log-in - Update collection and receipt times</em></p>
</div>

<li><strong>Result the Tests</strong>
    <ul>
    <li>Launch <strong>Accession Result Entry</strong> from the App Bar</li>
    <li>Pull up the accession using the accession number from the printed label</li>
    <li>Manually enter results from your instrument printout</li>
    <li>Enter results for each test in the Result field</li>
    </ul>
</li>

<div style="text-align: center; margin: 20px 0;">
<img src="{images_b64['result_entry']}" style="max-width: 100%; border: 2px solid #0066cc; border-radius: 6px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);" alt="Accession Result Entry">
<p style="font-size: 9pt; color: #666; margin-top: 8px;"><em>Figure 6: Accession Result Entry - Manually enter results from printouts</em></p>
</div>

<li><strong>Verify Results</strong>
    <ul>
    <li>After all results have been inputted correctly, hit <strong>Verify</strong></li>
    <li>Review all values before final verification</li>
    <li>Add comment "Reported during Downtime - Manual Entry" for audit trail</li>
    </ul>
</li>
</ol>
</div>

<div class="warning-box">
<h3>Important Reminders for Downtime Recovery</h3>
<ul>
<li><strong>All downtime specimens</strong> must be accessioned with proper collection/receive times</li>
<li><strong>Critical values</strong> reported verbally during downtime must be documented in LIS when system is restored</li>
<li><strong>Group specimens</strong> with same Cerner number (one patient) together</li>
<li><strong>STAT samples</strong> must be processed first upon system restoration</li>
<li><strong>Routine samples</strong> should be processed, labeled, and tracked after STAT completion</li>
<li><strong>Retain all downtime documentation</strong> (worksheets, printouts, requisitions) for compliance</li>
</ul>
</div>
</div>
'''

def create_epic_cerner_workflow_section():
    """Create Epic to Cerner workflow section."""
    return '''
<div class="section" id="epic-cerner-workflow">
<h2>8B. EPIC-TO-CERNER ORDERING WORKFLOW</h2>

<div class="key-concept">
<h3>Normal Operations (No Downtime)</h3>
<p>In normal operations, the workflow is seamless:</p>
<ol>
<li><strong>Provider enters orders in Epic</strong> → Orders automatically transmitted to Cerner LIS</li>
<li><strong>Lab staff prints labels from Cerner</strong> → Specimens collected and labeled</li>
<li><strong>Specimens analyzed</strong> → Results automatically interface from instruments to Cerner</li>
<li><strong>Results transmitted from Cerner to Epic</strong> → Provider views results in patient chart</li>
</ol>
</div>

<div class="emergency-box">
<h3>LIS Server Downtime: Epic and Cerner Operational, But Interface Down</h3>
<p>When the LIS server fails but Epic and Cerner systems remain operational individually:</p>

<h4>Impact:</h4>
<ul>
<li>Epic CANNOT send orders to Cerner automatically</li>
<li>Cerner CANNOT receive orders from Epic</li>
<li>Lab instruments CANNOT connect to Cerner to receive orders or transmit results</li>
<li>Cerner CANNOT send results back to Epic automatically</li>
</ul>

<h4>Phase 1: Communication and Activation</h4>
<ol>
<li><strong>IS Department Notification:</strong> Hospital IS department is immediately notified of interface failure</li>
<li><strong>Epic Alert:</strong> Providers see broadcast message about lab interface issue in Epic</li>
<li><strong>Lab Notification:</strong> Laboratory is alerted to interface failure</li>
<li><strong>Activate Manual Procedures:</strong> Both clinical staff and lab staff switch to paper-based workflows</li>
</ol>

<h4>Phase 2: Specimen Collection and Processing</h4>
<div class="procedure-section">
<p><strong>Step 1: Manual Epic Requisition</strong></p>
<ul>
<li>Provider or nurse fills out pre-printed downtime requisition form manually</li>
<li>Include: Patient demographics (name, DOB, MRN), ordering doctor, specific tests requested</li>
<li>This form cannot be transmitted electronically to Cerner</li>
</ul>

<p><strong>Step 2: Manual Specimen Labeling</strong></p>
<ul>
<li>Collection staff CANNOT print barcode labels from Cerner (no orders received)</li>
<li>Manually write patient information on specimen container</li>
<li>Use blank labels with unique downtime accession number (DT-MMDD-###)</li>
<li>Log accession number in paper logbook</li>
<li>Required on label:
    <ul>
    <li>Cerner Number (if available)</li>
    <li>Patient's Name</li>
    <li>Medical Record #</li>
    <li>Test, collection time, initials</li>
    </ul>
</li>
</ul>

<p><strong>Step 3: Lab Order Entry in Cerner</strong></p>
<ul>
<li>When specimen and paper requisition arrive at lab, accessioning clerks manually enter patient information into Cerner</li>
<li>Enter ALL requested test orders based on paper requisition form</li>
<li>Cerner generates its own internal accession number</li>
<li>Print barcode labels from Cerner for instrument processing</li>
</ul>

<p><strong>Step 4: Analyzer Operation (Standalone Mode)</strong></p>
<ul>
<li>Lab instruments must be operated in standalone mode (no LIS connection)</li>
<li>Lab staff manually enter test orders into instrument itself</li>
<li>Results print directly from instrument (not transmitted to Cerner)</li>
<li>Staff retains printouts for later manual data entry</li>
</ul>

<p><strong>Step 5: Manual Result Reporting</strong></p>
<ul>
<li><strong>Critical Values:</strong> Immediately call to patient's unit, document call on paper requisition</li>
<li><strong>Routine Results:</strong> Fax or physically deliver to clinical units</li>
<li><strong>Provider Follow-up:</strong> Ordering providers must actively contact lab for results</li>
</ul>
</div>

<h4>Phase 3: Recovery and Data Reconciliation</h4>
<div class="procedure-section">
<p><strong>When LIS Server is Restored:</strong></p>
<ol>
<li><strong>IT Notification:</strong> IT staff restores interface and notifies lab and clinical departments</li>
<li><strong>Manual Result Entry:</strong>
    <ul>
    <li>Lab staff manually enter results from instrument printouts into Cerner</li>
    <li>Use actual collection and receive times from downtime documents</li>
    <li>Add comment: "Reported during Downtime - Manual Entry"</li>
    </ul>
</li>
<li><strong>Interface Transmission:</strong>
    <ul>
    <li>As Cerner records are updated, restored interface transmits results to Epic</li>
    <li>Final verified results appear in patient's Epic chart</li>
    </ul>
</li>
<li><strong>Provider Reconciliation:</strong>
    <ul>
    <li>Clinical staff review results in Epic</li>
    <li>Reconcile against manual paper-based results received during downtime</li>
    <li>Epic may have features to link manual results with original electronic orders</li>
    </ul>
</li>
<li><strong>Document Retention:</strong>
    <ul>
    <li>Retain ALL manual requisitions, logbooks, and instrument printouts</li>
    <li>Required for regulatory and quality assurance purposes</li>
    </ul>
</li>
</ol>
</div>
</div>

<div class="critical-box">
<h3>Key Differences: LIS Server Down vs Full System Down</h3>
<table>
<thead>
<tr>
<th>Scenario</th>
<th>Epic Status</th>
<th>Cerner Status</th>
<th>Instruments</th>
<th>Workflow</th>
</tr>
</thead>
<tbody>
<tr>
<td>Full System Down</td>
<td>Down</td>
<td>Down</td>
<td>Standalone only</td>
<td>Complete manual process</td>
</tr>
<tr>
<td>LIS Server Down</td>
<td>Operational</td>
<td>Operational</td>
<td>Standalone only</td>
<td>Manual orders, electronic tracking</td>
</tr>
<tr>
<td>Cerner Only Down</td>
<td>Operational</td>
<td>Down</td>
<td>Down</td>
<td>Epic orders, manual lab processing</td>
</tr>
<tr>
<td>Normal Operations</td>
<td>Operational</td>
<td>Operational</td>
<td>Interfaced</td>
<td>Fully automated</td>
</tr>
</tbody>
</table>
</div>
</div>
'''

def main():
    print("Reading Downtime SOP file...")
    with open(SOP_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    print("Converting images to base64...")
    images_b64 = {
        'patient_search': read_image_as_base64(os.path.join(IMAGE_DIR, "Order Not In Cerner.jpg")),
        'add_orders': read_image_as_base64(os.path.join(IMAGE_DIR, "Add Orders to Scratchpad.jpg")),
        'submit_orders': read_image_as_base64(os.path.join(IMAGE_DIR, "Submit Orders.jpg")),
        'collection_inquiry': read_image_as_base64(os.path.join(IMAGE_DIR, "Orders in Cerner.jpg")),
        'specimen_login': read_image_as_base64(os.path.join(IMAGE_DIR, "Specimen Log-in.jpg")),
        'result_entry': read_image_as_base64(os.path.join(IMAGE_DIR, "Accession Result Entry.jpg"))
    }

    print("Creating new sections...")
    specimens_section = create_specimens_without_requisition_section()
    cerner_section = create_cerner_recovery_section(images_b64)
    epic_section = create_epic_cerner_workflow_section()

    # Find insertion points
    print("Finding insertion points...")

    # 1. Add specimens without requisition to Section 12 (Specimen Management)
    specimen_mgmt_pattern = r'(<div class="section" id="specimen">.*?<h2>12\. SPECIMEN MANAGEMENT DURING DOWNTIME</h2>)'
    content = re.sub(
        specimen_mgmt_pattern,
        r'\1' + '\n' + specimens_section,
        content,
        flags=re.DOTALL
    )

    # 2. Add Cerner recovery after Section 8 (LIS Downtime)
    # Find the end of section 8
    section_8_end_pattern = r'(</div>\s*<!-- SECTION 9: ANALYZER-SPECIFIC DOWNTIME -->)'
    content = re.sub(
        section_8_end_pattern,
        '\n' + cerner_section + '\n' + epic_section + r'\n\1',
        content,
        flags=re.DOTALL
    )

    # 3. Update table of contents
    toc_pattern = r'(<li><a href="#lis">8\. LIS Downtime</a></li>)'
    toc_addition = r'\1\n<li><a href="#cerner-recovery">8A. Cerner Recovery</a></li>\n<li><a href="#epic-cerner-workflow">8B. Epic-Cerner Workflow</a></li>'
    content = re.sub(toc_pattern, toc_addition, content)

    print(f"Writing updated SOP to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✓ Successfully updated Downtime SOP!")
    print(f"\nSummary of changes:")
    print("  1. Added 'Specimens Without Requisition' to Section 12")
    print("  2. Added Section 8A: 'Cerner Downtime Recovery Procedures' with 6 embedded images")
    print("  3. Added Section 8B: 'Epic-to-Cerner Ordering Workflow'")
    print("  4. Updated Table of Contents with new sections")
    print(f"\nOutput file: {OUTPUT_FILE}")
    print(f"File size: {os.path.getsize(OUTPUT_FILE) / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    main()
