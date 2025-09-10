# 🧠 Notion Database Import Guide - Kaiser Permanente Lab Alerts

## Step 1: Create Notion Integration

### 1.1 Get Your Notion API Token
1. Go to [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click **"+ New Integration"**
3. Name: `Kaiser Lab Automation`
4. Workspace: Select your Kaiser workspace
5. Click **"Submit"**
6. **Copy the Integration Token** (starts with `secret_`)

### 1.2 Create Lab Alerts Database
1. In Notion, click **"+ New Page"**
2. Select **"Table"** template
3. Title: `🚨 Kaiser Lab Alerts & Tasks`

## Step 2: Configure Database Properties

Delete default properties and add these exact columns:

### Alert Properties
```
Property Name: Alert ID
Type: Title
```

```
Property Name: Severity
Type: Select
Options: 
- 🔴 Critical
- 🟠 High  
- 🟡 Medium
- 🔵 Low
- 🟣 Compliance
```

```
Property Name: Message
Type: Text
```

```
Property Name: Keywords Detected
Type: Multi-select
Options: (leave empty - will auto-populate)
```

```
Property Name: Timestamp
Type: Date & Time
```

```
Property Name: Department
Type: Select
Options:
- Chemistry
- Hematology
- Microbiology
- Blood Bank
- Phlebotomy
- IT Systems
- Administration
```

```
Property Name: Assigned To
Type: People
```

```
Property Name: Status
Type: Select
Options:
- 🟥 Open
- 🟨 In Progress
- 🟩 Resolved
- 🟦 Escalated
- ⚫ Closed
```

```
Property Name: Response Time
Type: Number (Minutes)
```

```
Property Name: Follow-up Required
Type: Checkbox
```

```
Property Name: Resolution Notes
Type: Text
```

## Step 3: Share Database with Integration

1. Click **"Share"** button (top right of your database)
2. Click **"Invite"**
3. Search for your integration: `Kaiser Lab Automation`
4. Select it and click **"Invite"**
5. **Copy the Database ID** from the URL
   - URL format: `https://notion.so/workspace/DATABASE_ID?v=VIEW_ID`
   - DATABASE_ID is the long string between workspace/ and ?v=

## Step 4: Test Database Connection

### 4.1 Test with curl (Optional)
```bash
curl -X POST https://api.notion.com/v1/pages \
  -H "Authorization: Bearer YOUR_INTEGRATION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "YOUR_DATABASE_ID"},
    "properties": {
      "Alert ID": {"title": [{"text": {"content": "TEST-001"}}]},
      "Severity": {"select": {"name": "🔴 Critical"}},
      "Message": {"rich_text": [{"text": {"content": "Test alert from setup"}}]},
      "Status": {"select": {"name": "🟥 Open"}}
    }
  }'
```

### 4.2 Expected Response
```json
{
  "object": "page",
  "id": "page-id",
  "created_time": "2024-01-01T00:00:00.000Z",
  "properties": {...}
}
```

## Step 5: Configure Database Views

### 5.1 Create "Active Alerts" View
1. Click **"+ New View"** 
2. Name: `🚨 Active Alerts`
3. View Type: `Table`
4. Filter: `Status` does not equal `🟩 Resolved` AND `Status` does not equal `⚫ Closed`
5. Sort: `Severity` (🔴 Critical first), then `Timestamp` (Newest first)

### 5.2 Create "Critical Dashboard" View  
1. Click **"+ New View"**
2. Name: `🔴 Critical Only`
3. View Type: `Gallery`
4. Filter: `Severity` equals `🔴 Critical`
5. Sort: `Timestamp` (Newest first)

### 5.3 Create "Department View"
1. Click **"+ New View"**
2. Name: `🏥 By Department` 
3. View Type: `Board`
4. Group By: `Department`
5. Sort: `Timestamp` (Newest first)

## ✅ Notion Setup Complete!

**Save These Values:**
- **Integration Token**: `secret_XXXXXXXXX`
- **Database ID**: `XXXXXXXXXXXXXXXX`

You'll need these for Power Automate configuration.

---

## 🔄 Next: Power Automate Setup

Continue to `power_automate_import_guide.md` to complete the integration.