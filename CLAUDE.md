# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This codebase contains multiple healthcare informatics and bioinformatics projects focused on laboratory systems, data analysis, and academic coursework. The primary technologies are Python (for backend/data processing) and React (for frontend applications).

## Key Projects

### 1. Critical-Values-Alert-System
**Location**: `/Users/ugochi141/Critical-Values-Alert-System/`
**Purpose**: Lab TAT (Turnaround Time) monitoring dashboard using Streamlit
**Commands**:
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### 2. HL7-Lab-Results-Pipeline
**Location**: `/Users/ugochi141/HL7-Lab-Results-Pipeline/`
**Purpose**: Production-ready pipeline for processing HL7 v2.x lab result messages
**Commands**:
```bash
# Install dependencies
pip install -r HL7-Lab-Results-Pipeline/requirements.txt

# Run the pipeline
python HL7-Lab-Results-Pipeline/hl7_lab_pipeline.py
```

### 3. Frontend (Lab Order Dashboard)
**Location**: `/Users/ugochi141/frontend/lab-order-dashboard-frontend/`
**Purpose**: React-based frontend for lab order tracking
**Commands**:
```bash
# Install dependencies
npm install

# Run development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

### 4. Bioinformatics Projects
**Locations**: 
- `/Users/ugochi141/BioPythonAssignment/`
- `/Users/ugochi141/JHU_Bioinformatics_Portfolio/`
- `/Users/ugochi141/huntington_analysis/`

**Purpose**: Academic assignments and gene analysis projects
**Commands**:
```bash
# Run Python scripts directly
python script_name.py
```

## Architecture

### Healthcare Systems Architecture
The codebase implements a laboratory information system with:
- **Data Ingestion**: HL7 message processing pipeline
- **Data Processing**: Python-based analysis and transformation
- **Data Visualization**: Streamlit dashboards for monitoring
- **Frontend**: React application for user interface
- **Integration**: Support for Epic Beaker and Cerner systems

### Key Technologies
- **Python 3.7+**: Main backend language
- **React 18+**: Frontend framework
- **Streamlit**: Dashboard framework
- **HL7 v2.x**: Healthcare messaging standard
- **pandas/numpy**: Data analysis
- **matplotlib/seaborn**: Visualization

### Data Flow
1. HL7 messages are received and parsed by the pipeline
2. Lab results are processed and critical values identified
3. Data is stored and made available to dashboards
4. Streamlit app provides real-time monitoring
5. React frontend offers user interaction

## Development Guidelines

### Python Projects
- Use virtual environments for dependency isolation
- Follow PEP 8 style guidelines
- Add type hints for function parameters
- Document functions with docstrings

### React Projects
- Use functional components with hooks
- Follow ESLint configuration
- Write tests for components
- Use axios for API calls

### HL7 Processing
- Validate message structure before processing
- Handle encoding issues (ISO-8859-1, UTF-8)
- Log all message processing for audit trail
- Implement error handling for malformed messages

## Common Tasks

### Adding New HL7 Message Types
1. Add parser in `hl7_lab_pipeline.py`
2. Create transformation logic for the message type
3. Update documentation with field mappings
4. Test with sample messages

### Creating New Dashboard Views
1. Add new page in Streamlit app
2. Create data processing functions
3. Implement visualization components
4. Update navigation in sidebar

### Updating Frontend Components
1. Create component in `src/components/`
2. Add to appropriate page/route
3. Connect to backend API
4. Write component tests

## Important Notes

- The projects handle healthcare data - ensure HIPAA compliance
- HL7 messages may contain PHI - use mock data for testing
- Critical value thresholds vary by lab - make configurable
- Support multiple lab systems (Epic, Cerner) with different formats

## Troubleshooting Guide

### JavaScript Property Mismatch Issues

**Symptom:** Table shows "No data" despite data existing in the HTML/JSON
**Common Cause:** Property name mismatch between JavaScript rendering code and data structure

**Diagnostic Steps:**
1. Check browser console for JavaScript errors (TypeError, undefined property)
2. Inspect the data structure field names (e.g., 'dept', 'role', 'assignment')
3. Compare with JavaScript code accessing those properties
4. Look for `.forEach()` loops and template literals using `${variable}`

**Example Fix Pattern:**
- Data structure: `{name: 'John', dept: 'MLS'}`
- Broken code: `${s.role.toLowerCase()}`
- Fixed code: `${s.dept.toLowerCase()}`

**Key Files:**
- `/Users/ugochi141/Documents/largo-lab-portal/Schedules/Daily Schedule.html`
- GitHub: https://github.com/ugochi141/largo-lab-portal

**Resolution Steps:**
1. Identify the exact property name in the data structure
2. Search for all references to the incorrect property name in the code
3. Replace with the correct property name
4. Test locally before committing
5. Commit with descriptive message explaining the fix
6. Push to GitHub and verify deployment

## Largo Lab Portal - Daily Schedule Standards

### Staff Ordering Convention

**IMPORTANT:** Always order staff by shift start time (earliest to latest) in the Daily Schedule HTML.

#### Phlebotomy Staff Order (by startTime)
Order staff entries by their `startTime` value in ascending order:
- 6:00am shifts (startTime: 6)
- 7:00am shifts (startTime: 7)
- 8:00am shifts (startTime: 8)
- 9:00am shifts (startTime: 9)
- 12:00pm shifts (startTime: 12)
- 1:30pm shifts (startTime: 13.5)
- 2:00pm shifts (startTime: 14)
- 5:00pm shifts (startTime: 17)

#### Laboratory Technicians Order (by startTime)
Order staff entries by their `startTime` value in ascending order:
- 7:30am shifts (startTime: 7.5) - Day shift techs
- 8:00am shifts (startTime: 8) - Day shift techs
- 3:30pm shifts (startTime: 15.5) - Evening shift techs
- 9:30pm shifts (startTime: 21.5) - Night shift techs
- 11:30pm shifts (startTime: 23.5) - Night shift techs
- 12:00am shifts (startTime: 0) - Night shift techs (midnight start)

**Note:** Night shifts that start at midnight (12:00am) have `startTime: 0` and should be placed LAST in the list, even though 0 < other values. This maintains chronological day flow.

#### Data Structure Format
```javascript
{
    name: 'Full Name',
    nickname: 'Nickname',
    assignment: 'Role Description', // for phleb
    dept: 'MLA/MLT/MLS',           // for lab techs
    shift: '7:30a-4p',
    breaks: 'Break 1: 9:45a-10:00a | Lunch: 11:30a-12:00p | Break 2: 2:45p-3:00p',
    startTime: 7.5
}
```

**IMPORTANT - Department Field Convention:**
- **ALWAYS use "MLS"** for Medical Laboratory Scientists (Medical Technologists)
- **NEVER use "MT"** - this is incorrect terminology
- Medical Laboratory Scientists = MLS (correct)
- Medical Technologists = MLS (correct)
- MT = INCORRECT, always change to MLS

**When Adding New Schedule Dates:**
1. Always order phlebotomy staff by startTime (ascending)
2. Always order laboratory staff by startTime (ascending, with midnight shifts last)
3. Maintain consistent formatting with existing entries
4. Stagger break times to avoid overlaps (15-min intervals)
5. Use October 9, 2025 schedule as the reference template

### Phlebotomy Role Assignments & Accountability Standards

**CRITICAL - Always Use Correct Nicknames:**

**Phlebotomy Staff:**
- Christina Bolden-Davis → nickname: 'Christina'
- Johnette Brooks → nickname: 'Netta' (NOT 'Johnette')
- Raquel Grayson → nickname: 'Raquel' (CORRECTION: USE 'Raquel' NOT 'Rachel')
- Manoucheca Onuma → nickname: 'Mimi'
- Youlana Miah → nickname: 'Youlana'
- Farah Moise → nickname: 'Farah'
- Anne Saint Phirin → nickname: 'Anne'
- Emmanuella Theodore → nickname: 'Emmanuella'
- Micaela Scarborough → nickname: 'Micaela'
- Shannon Pilkington → nickname: 'Shannon'
- Stephanie Dodson → nickname: 'Stephanie'
- Nichole Fauntleroy → nickname: 'Nichole'
- Danalisa Hayes → nickname: 'Danalisa'
- Taric White → nickname: 'Taric'
- Tamika Nettles → nickname: 'Tamika'
- Marilyn Ortiz → nickname: 'Marilyn'

**Laboratory Technicians:**
- Jacqueline Liburd → nickname: 'Jackie'
- Emmanuel Lejano → nickname: 'Boyet'
- Maxwell Booker → nickname: 'Booker' (NOT 'Maxwell')
- Ogheneochuko Eshofa → nickname: 'Tracy'
- Lorraine Blackwell → nickname: 'Lorraine'
- Emily Creekmore → nickname: 'Emily'
- Ingrid Benitez-Ruiz → nickname: 'Ingrid'
- Lionel Ndifor → nickname: 'Lionel'
- Albert Che → nickname: 'Albert'
- George Etape → nickname: 'George'

**Role Assignment Standards (Non-Negotiable):**

**IMPORTANT - Assignment Title Format:**
- Always list primary role first: "Draw Patients/[specific role]"
- Examples: "Draw Patients/Opener", "Draw Patients/Runner", "Draw Patients/Hot Seat"
- Exception: "Processor" stands alone (no "Draw Patients/" prefix)
- Exception: "Draw Patients (Backup Processor)" uses parentheses

**Opener (Phleb)**
- Assignment: 'Draw Patients/Opener'
- Core Responsibility: Temp check in phleb area. Clean and stock draw stations.
- Accountability: Area must be fully stocked and ready for shift start. Check tubes expiration dates at each station.
- Who: First shift of the day

**Processor (Dayshift)**
- Assignment: 'Processor'
- Core Responsibility: Process for the entire shift.
- Accountability: Do not leave processing station until end of shift. Remain processing until your shift is complete and you have passed down the handoff sheet to evening shift. Must complete the 10am run!
- Who: Phlebotomists trained in processing

**Backup Processor**
- Assignment: 'Draw Patients (Backup Processor)'
- Core Responsibility: Assist processing when business allows.
- Accountability: When processing assistance isn't needed, you are drawing patients.
- Who: Whoever can process for day shift can be Backup Processor

**Evening Processor**
- Assignment: 'Processor'
- Core Responsibility: Finalize logs and function as Processor 2/3 initially.
- Accountability: Do not interrupt the dayshift processing workflow. Must place both day and evening shift communication logs in the designated box, sorted by date.
- Who: Evening phlebotomists trained in processing

**Hot Seat**
- Assignment: 'Draw Patients/Hot Seat'
- Core Responsibility: Flexible role coverage as business needs dictate
- Who: Whoever is not a closer in evening shifts

**Runner**
- Assignment: 'Draw Patients/Runner'
- Core Responsibility: Deliver labs every 30 minutes
- Accountability: Specimens must be delivered promptly to Lab (AUC/MOB) for prompt testing

**Closer**
- Assignment: 'Draw Patients/Closer'
- Core Responsibility: Restock phlebotomy area.
- Accountability: Area must be left complete and ready for the next shift. Check tubes expiration dates at each station.
- Who: Last shift or 2nd to last shift of the day

**ROTATION POLICY:**
- Rotate phlebotomists on what they can do
- Rotate ALL staff on bench assignments

**Processing Training Status:**
- ✓ Fully Trained (Day): Anne Saint Phirin, Farah Moise, Manucheca Onuma, Youlana Miah, Christina Bolden-Davis, Emmanuella Theodore
- ✓ Fully Trained (Evening): Danalisa Hayes, Nichole Fauntleroy
- ⚠ Needs Training: Netta (Johnette Brooks), Micaela Scarborough, Taric White

---

## Laboratory Bench Assignment Standards

### Staffing-Based Bench Rotations

**CRITICAL RULE:** Rotate ALL staff on bench assignments

#### AUC Day Shift (Two Techs)
**Assignment Split:**
- **AUC Front:** Processing/Urines, Kits, Stago
- **AUC Back:** Hematology, Chemistry, Molecular

#### MOB Day Shift (One Tech + One MLA)
**Tech Assignment:**
- MOB Quality Control and Maintenance Operations

**MLA Assignment:**
- MOB - Assist with QC/Maint, Inventory
- SQA Daily
- Hematek Daily QC
- Previ Gram

#### AUC Evening Shift (Three Techs)
**Assignment Split:**
- **Tech 1:** Urines, Kits, Stago
- **Tech 2:** Processing
- **Tech 3:** Hematology, Chemistry, Molecular

### Specific QC Assignments by Staff Member

#### Maxwell Booker (Booker) - MOB
- Pure 1 QC @7:30am (Daily)
- Kits QC (Daily)
- Sysmex Startup/QC (Daily)
- Hematek Startup/QC (Daily)
- Previ Gram Stain (Daily)
- Stago Maint
- Beads Maint
- Log QC

#### Lorraine Blackwell - MOB
- Assist with QC/Maint
- Inventory Management
- Novus Weekly (Wednesdays)

#### Emily Creekmore - AUC Back
- MedTox QC (Daily)
- Sysmex Startup/QC (Daily)
- Hematek Startup/QC (Daily)
- Stago Maint
- Log QC

#### Ingrid Benitez-Ruiz - AUC Front
- Processing
- Kits QC (Daily)
- Stago Maint
- Log QC

### Daily Maintenance Assignments (All Staff)

**Stago Maintenance:**
- ESR 10% Check QC (Daily)
- Stago Maint
- Log QC

**Universal Requirements (EVERYONE):**
- Wipe Benches
- Clean Microscopes

### Lead Duties Assignments

**Ingrid Benitez-Ruiz:**
- Lead Duties on Mondays and Thursdays

**Sam (Samantha):**
- Lead Duties when 3 techs work the bench

### TempTrak Temperature Monitoring (10/13/25 - 10/17/25)

**AUC Location:**
- 9:00am check
- 4:00pm check
- 12:00am (midnight) check

**MOB Location:**
- 9:00am check
- 4:00pm check

**Note:** Temperature monitoring must be documented per CLIA/CAP requirements. Ensure all checks are logged in TempTrak system.