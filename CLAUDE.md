# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 🔥 CRITICAL - # TO MEMORIZE

### 1. **Always Use MLS, NEVER MT**
- Medical Laboratory Scientists = **MLS** (correct)
- Medical Technologists = **MLS** (correct)
- MT = **INCORRECT** - always change to MLS

### 2. **GitHub Pages Deployment - Dynamic Date Required**
When updating https://ugochi141.github.io/largo-lab-portal/:
- **ALWAYS verify:** `let currentDate = new Date();` (dynamic)
- **NEVER use:** `let currentDate = new Date('2025-10-13');` (hardcoded)
- **Location:** Line ~1487 in `Daily Schedule.html`
- **Why:** Hardcoded dates show wrong schedule regardless of data updates

### 3. **Critical Nicknames**
- Johnette Brooks → **'Netta'** (NOT 'Johnette')
- Raquel Grayson → **'Raquel'** (NOT 'Rachel')
- Maxwell Booker → **'Booker'** (NOT 'Maxwell')
- Jacqueline Liburd → **'Jackie'** (NOT 'Jacqueline')
- Emmanuel Lejano → **'Boyet'**
- Ogheneochuko Eshofa → **'Tracy'**

### 4. **Rotation Policies**
- **Rotate phlebotomists on what they can do**
- **Rotate ALL staff on bench assignments**

### 5. **Assignment Title Format**
- Standard: "Draw Patients/[role]" → "Draw Patients/Opener", "Draw Patients/Runner"
- Exception: "Processor" (stands alone, no prefix)
- Exception: "Draw Patients (Backup Processor)" (uses parentheses)

### 6. **QC/Maintenance Schedule Quick Reference**

**Weekly Tasks:**
- **Tuesday:** Previ Gram (MOB day), Novus (AUC night after 3am)
- **Wednesday:** Novus (MOB day), Stago (Both evening)
- **Thursday:** GeneXpert (Both night)
- **Saturday:** Sysmex XN Shutdown (9pm AUC, 10pm MOB)
- **Weekly:** Hematek (Both)

**Biweekly Tasks:**
- **Every other Friday 10pm:** Pure 1 (MOB) - starts 10/04/25
- **Every other Saturday 3am:** Pure 2 (AUC) - starts 10/11/25

**Monthly Tasks:**
- **2nd Wednesday:** Hematek (Both day), GeneXpert (Both night)
- **2nd Thursday 9pm:** Stago (Both evening)
- **3rd Tuesday:** Previ Gram (MOB day)
- **3rd Wednesday:** MedTox (AUC day)
- **3rd Thursday:** Novus (MOB day)
- **3rd Saturday 3am:** Pure Analyzers (Both night)

### 7. **Schedule Data Synchronization - Daily Schedule as Source of Truth**

**CRITICAL:** Daily Schedule data MUST automatically populate and update both:
1. **Visual Coverage Schedule** (`Scheduler.html`)
2. **Call Out Tracker** (`Scheduler1.html`)

**How it works:**
- Daily Schedule is the **single source of truth** for all schedule data
- `ScheduleSync` object handles automatic synchronization via localStorage
- localStorage keys: `dailyScheduleData`, `visualScheduleData`, `callOutScheduleData`
- When Daily Schedule updates, it MUST sync data to all three pages for corresponding dates
- Visual Coverage and Call Out Tracker pages read from localStorage to display synced data

**File Paths:**
- **Source:** `/Users/ugochi141/Documents/largo-lab-portal/Schedules/Daily Schedule.html`
- **Target 1 (Visual Coverage):** `/Users/ugochi141/Documents/largo-lab-portal/Schedules/Scheduler.html`
- **Target 2 (Call Out Tracker):** `/Users/ugochi141/Documents/largo-lab-portal/Schedules/Scheduler1.html`

**GitHub Pages URLs:**
- **Daily Schedule:** https://ugochi141.github.io/largo-lab-portal/Schedules/Daily%20Schedule.html
- **Visual Coverage:** https://ugochi141.github.io/largo-visual-coverage-schedule/
- **Call Out Tracker:** https://ugochi141.github.io/largo-call-out-tracker/

**Verification Steps:**
1. Update schedule data in Daily Schedule.html
2. Verify `ScheduleSync.syncFromDailySchedule(scheduleData)` is called
3. Check localStorage for updated `visualScheduleData` and `callOutScheduleData`
4. Open Visual Coverage Schedule (Scheduler.html) and verify it displays synced data for the date
5. Open Call Out Tracker (Scheduler1.html) and verify it displays synced data for the date

### 8. **QC/Maintenance Staff Assignments - Daily/Weekly/Biweekly/Monthly**

**CRITICAL:** MLA can ONLY do Urines and Kits QC. All other QC must be assigned to MLT or MLS.

#### **DAILY QC Assignments:**

**MOB Day Shift (7:30am start):**
- **Booker (MLT)**: Pure 1 QC @7:30am, Kits QC, Sysmex Startup/QC, Hematek Startup/QC, Previ Gram Stain, Stago Maint, Beads Maint, Log QC
- **Lorraine (MLA)**: Assist with QC/Maint, Inventory, SQA Daily, Urines, Kits ONLY

**AUC Day Shift (7:30am start):**
- **AUC Front Tech (MLT/MLS rotating)**: Kits QC, Stago Maint, Processing, Log QC
- **Emily (MLT)**: Pure 2 QC @3:00am (night carryover), MedTox QC, Sysmex Startup/QC, Hematek Startup/QC, Stago Maint, Log QC

**AUC Evening Shift (3:30pm start):**
- **Tracy (MLT)**: Urines, Kits, Stago, ESR 10% Check QC, Stago Maint, Log QC
- **Lionel (MLT)**: Hematology, Chemistry, Molecular QC, Log QC
- **Albert (MLS)**: Hematology, Chemistry, Molecular QC, Log QC

**AUC Night Shift:**
- **Boyet (MLT)**: 9:30p-6a, AUC Night Coverage, MiniSed QC, GeneXpert QC
- **George (MLS)**: 11:30p-8a, AUC Night Coverage, MiniSed QC, GeneXpert QC
- **Jackie (MLS)**: 12a-6:30a, AUC Night Coverage, MiniSed QC

**ALL STAFF (Daily):**
- Wipe Benches, Clean Microscopes, Log QC

---

#### **WEEKLY QC Assignments:**

**Tuesday:**
- **Previ Gram Stain (MOB)** - Day shift: Booker (MLT), Lorraine (MLA can assist) | **[WEEKLY]**
- **Novus (AUC)** - Night shift after 3am: George (MLS) | **[WEEKLY]**

**Wednesday:**
- **Novus (MOB)** - Day shift: Lorraine (MLA) | **[WEEKLY]**
- **Stago (Both AUC & MOB)** - Evening shift: Tracy (MLT), Lionel (MLT), Albert (MLS) | **[WEEKLY]**

**Thursday:**
- **GeneXpert (Both AUC & MOB)** - Night shift: George (MLS), Boyet (MLT) | **[WEEKLY]**

**Saturday:**
- **Sysmex XN Shutdown (AUC)** - 9:00 PM: Evening shift (Tracy/Lionel/Albert) | **[WEEKLY]**
- **Sysmex XN Shutdown (MOB)** - 10:00 PM: Evening shift (assigned tech) | **[WEEKLY]**
- **Hematek (Both AUC & MOB)** - Day shift: Booker (MLT-MOB), Emily (MLT-AUC) | **[WEEKLY]**

---

#### **BIWEEKLY QC Assignments:**

**Pure Analyzer 1 (MOB):**
- **Every other Friday, 10:00 PM** - Evening shift tech (MLT/MLS)
- **Start Date:** 10/04/25
- **Next dates:** 10/18/25, 11/01/25, 11/15/25... | **[BIWEEKLY]**

**Pure Analyzer 2 (AUC):**
- **Every other Saturday, 3:00 AM** - Night shift: George (MLS)
- **Start Date:** 10/11/25
- **Next dates:** 10/25/25, 11/08/25, 11/22/25... | **[BIWEEKLY]**

---

#### **MONTHLY QC Assignments:**

**2nd Wednesday of Month:**
- **Hematek (Both)** - Day shift: Booker (MLT-MOB), Emily (MLT-AUC) | **[MONTHLY]**
- **GeneXpert (Both)** - Night shift: George (MLS), Boyet (MLT) | **[MONTHLY]**

**2nd Thursday of Month:**
- **Stago (Both)** - 9:00 PM Evening shift: Tracy (MLT), Lionel (MLT), Albert (MLS) | **[MONTHLY]**

**3rd Tuesday of Month:**
- **Previ Gram Stain (MOB)** - Day shift: Booker (MLT), Lorraine (MLA can assist) | **[MONTHLY]**

**3rd Wednesday of Month:**
- **MedTox (AUC)** - Day shift: Emily (MLT) | **[MONTHLY]**

**3rd Thursday of Month:**
- **Novus (MOB)** - Day shift: Lorraine (MLA) | **[MONTHLY]**

**3rd Saturday of Month:**
- **Pure Analyzers (Both AUC & MOB)** - 3:00 AM Night shift: George (MLS) | **[MONTHLY]**

---

**MLA RESTRICTION REMINDER:**
- **Lorraine (MLA)** can ONLY perform: Urines, Kits QC, Assist with QC/Maint, Inventory, SQA Daily
- **ALL other QC** must be assigned to MLT or MLS staff

---

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

---

## QC and Maintenance Schedule

### Weekly Tasks

**Hematek (Both AUC & MOB):**
- Frequency: Weekly
- Assigned: Day shift staff

**Sysmex XN Shutdown:**
- **AUC:** Saturday evening, 9:00 PM
- **MOB:** Saturday evening, 10:00 PM
- Assigned: Evening shift staff

**Previ Gram Stain (MOB):**
- Frequency: Every Tuesday
- Assigned: Day shift (Booker, Lorraine)

**Novus (AUC):**
- Frequency: Every Tuesday night after 3:00 AM
- Assigned: Night shift (George)

**Novus (MOB):**
- Frequency: Every Wednesday day shift
- Assigned: Day shift (Lorraine)

**GeneXpert (Both AUC & MOB):**
- Frequency: Every Thursday night
- Assigned: Night shift (George)

**Stago (Both AUC & MOB):**
- Frequency: Every Wednesday evening
- Assigned: Evening shift (Tracy, Lionel, Albert)

---

### Biweekly Tasks

**Pure Analyzer 2 (AUC):**
- Frequency: Every other Saturday, 3:00 AM
- Start Date: 10/11/25
- Next: 10/25/25, 11/08/25, 11/22/25...
- Assigned: Night shift (George)

**Pure Analyzer 1 (MOB):**
- Frequency: Every other Friday, 10:00 PM
- Start Date: 10/04/25
- Next: 10/18/25, 11/01/25, 11/15/25...
- Assigned: Evening shift

---

### Monthly Tasks

**Hematek (Both locations):**
- Frequency: 2nd Wednesday of month
- Shift: Day shift
- Assigned: Booker (MOB), Emily (AUC)

**MedTox (AUC):**
- Frequency: 3rd Wednesday of month
- Shift: Day shift
- Assigned: Emily

**Previ Gram Stain (MOB):**
- Frequency: 3rd Tuesday of month
- Shift: Day shift
- Assigned: Booker, Lorraine

**Novus (MOB):**
- Frequency: 3rd Thursday of month
- Shift: Day shift
- Assigned: Lorraine

**GeneXpert (Both locations):**
- Frequency: 2nd Wednesday of month
- Shift: Night shift
- Assigned: George

**Stago (Both locations):**
- Frequency: 2nd Thursday of month, 9:00 PM
- Shift: Evening shift
- Assigned: Tracy, Lionel, Albert

**Pure Analyzers (Both AUC & MOB):**
- Frequency: 3rd Saturday of month, 3:00 AM
- Shift: Night shift
- Assigned: George

---

### QC Schedule Quick Reference

**Daily:**
- Pure 1 QC (MOB) - 7:30am
- Pure 2 QC (AUC) - 3:00am
- Kits QC, Sysmex, Hematek, MedTox, Stago, ESR 10%
- MiniSed QC, GeneXpert QC (night)
- Log QC, Wipe Benches, Clean Microscopes (ALL staff)

**Weekly:**
- Tuesday: Previ Gram (MOB), Novus (AUC - night)
- Wednesday: Novus (MOB - day), Stago (Both - evening)
- Thursday: GeneXpert (Both - night)
- Saturday: Sysmex XN Shutdown (9pm AUC, 10pm MOB)

**Biweekly:**
- Every other Friday 10pm: Pure 1 (MOB) - starts 10/04/25
- Every other Saturday 3am: Pure 2 (AUC) - starts 10/11/25

**Monthly:**
- 2nd Wednesday: Hematek, GeneXpert (night)
- 2nd Thursday 9pm: Stago
- 3rd Tuesday: Previ Gram (MOB)
- 3rd Wednesday: MedTox (AUC)
- 3rd Thursday: Novus (MOB)
- 3rd Saturday 3am: Pure Analyzers (Both)

---

## GitHub Pages Deployment Process

### # TO MEMORIZE - Proper GitHub Pages Update Workflow

**CRITICAL:** When updating the largo-lab-portal GitHub Pages site, follow this exact process:

#### Step 1: Update the Schedule Data (JavaScript Object)
1. Locate the schedule data in `/Users/ugochi141/Documents/largo-lab-portal/Schedules/Daily Schedule.html`
2. Find the appropriate date entry (e.g., `'2025-10-14': { phleb: [...], lab: [...] }`)
3. Update the JavaScript data structure with schedule changes
4. Ensure all nicknames, assignments, and roles are correct

#### Step 2: Verify Dynamic Date Handling
**CRITICAL CHECK:** Ensure the page uses dynamic date, NOT hardcoded dates
```javascript
// CORRECT (uses current date):
let currentDate = new Date();

// WRONG (hardcoded date will show wrong schedule):
let currentDate = new Date('2025-10-13');
```

**Location in file:** Search for `let currentDate = new Date` (around line 1487)
**Why this matters:** If hardcoded, the page will ALWAYS show that specific date's schedule, ignoring your data updates.

#### Step 3: Commit and Push Changes
```bash
cd "/Users/ugochi141/Documents/largo-lab-portal"
git add "Schedules/Daily Schedule.html"
git commit -m "Descriptive commit message"
git push
```

#### Step 4: Verify GitHub Pages Deployment
```bash
# Check latest deployment status
gh api repos/ugochi141/largo-lab-portal/deployments --jq '.[0] | {created_at, sha: .sha[0:7], environment, status}'

# Wait 30-60 seconds for deployment to complete
sleep 30

# Verify deployment succeeded
gh api repos/ugochi141/largo-lab-portal/deployments --jq '.[0].id' | xargs -I {} gh api repos/ugochi141/largo-lab-portal/deployments/{}/statuses --jq '.[0] | {state, created_at}'
```

Expected output: `"state": "success"`

#### Step 5: Verify Live Site
- Wait 1-2 minutes for CDN cache to clear
- Visit: https://ugochi141.github.io/largo-lab-portal/Schedules/Daily%20Schedule.html
- Check that the current date's schedule displays correctly
- Verify all updates are visible (callouts removed, new assignments, correct nicknames)

### Common GitHub Pages Issues

**Issue 1: "I pushed changes but the live site shows old data"**
- **Cause:** Hardcoded date in JavaScript (e.g., `new Date('2025-10-13')`)
- **Fix:** Change to `new Date()` to use current date dynamically
- **Location:** Line ~1487 in Daily Schedule.html

**Issue 2: "Deployment shows success but site not updating"**
- **Cause:** Browser cache or CDN cache delay
- **Fix 1:** Hard refresh browser (Cmd+Shift+R on Mac, Ctrl+Shift+R on Windows)
- **Fix 2:** Wait 2-3 minutes for CDN cache to expire
- **Fix 3:** Open in incognito/private browser window

**Issue 3: "Site shows JavaScript errors or blank tables"**
- **Cause:** Syntax error in schedule data (missing comma, bracket, quote)
- **Fix:** Check browser console for errors, validate JSON syntax
- **Prevention:** Always test locally before pushing

### GitHub Pages Configuration
- **Repository:** https://github.com/ugochi141/largo-lab-portal
- **Live Site:** https://ugochi141.github.io/largo-lab-portal/
- **Branch:** main
- **Deploy Source:** Legacy (root of main branch)
- **Auto-deploy:** Enabled (deploys on every push to main)
- **Typical Deploy Time:** 30-60 seconds

### Deployment Verification Checklist
- [ ] JavaScript data structure updated with correct schedule
- [ ] Date handling is dynamic (`new Date()` not hardcoded)
- [ ] All nicknames match CLAUDE.md reference list
- [ ] All "MT" changed to "MLS" (if applicable)
- [ ] Changes committed with descriptive message
- [ ] Changes pushed to main branch
- [ ] GitHub Pages deployment triggered
- [ ] Deployment status shows "success"
- [ ] Live site displays correct data (after cache clear)
- to memorize