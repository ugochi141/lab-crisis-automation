# 🔧 Notion Integration Setup Guide
## Kaiser Permanente Lab Automation System

### ✅ **Current Status**
- **API Connection**: ✅ Working
- **Token**: ✅ Valid (loaded from environment)
- **Database Access**: ❌ Needs sharing setup

---

## 🚀 **Quick Fix Instructions**

### **Step 1: Share Your Databases with Integration**

You need to share your existing databases with the Notion integration. Here's how:

#### **Performance Database** 
1. Go to your **Team Performance Dashboard**: https://www.notion.so/c1500b1816b14018beabe2b826ccafe9
2. Click the **"Share"** button (top right corner)
3. In the share dialog, type: **"Kaiser Permanente Lab Automation"**
4. Select your integration from the dropdown
5. Set permissions to **"Can edit"**
6. Click **"Invite"**

#### **Incident Database**
1. Go to your **Incident Tracking**: https://www.notion.so/cf2bb4448aff4324a602cb770cbae0a2
2. Click the **"Share"** button (top right corner)
3. Type: **"Kaiser Permanente Lab Automation"**
4. Select your integration and set to **"Can edit"**
5. Click **"Invite"**

#### **Lab Command Center Pages**
Share these pages with your integration:

1. **Lab Management Command Center**
   - URL: https://www.notion.so/Lab-Management-Command-Center-266d222751b3818996b4ce1cf18e0913
   - Click "Share" → Add integration → "Can edit"

2. **Lab Operations Command Center**
   - URL: https://www.notion.so/Lab-Operations-Command-Center-264d222751b38187966bdfd1055e10d6
   - Click "Share" → Add integration → "Can edit"

3. **Lab Operations**
   - URL: https://www.notion.so/Lab-Operations-264d222751b3819da42be04e2f399357
   - Click "Share" → Add integration → "Can edit"

#### **Team Workspace**
1. Go to your team workspace: https://www.notion.so/team/1cdd2227-51b3-818e-8bb7-004288f69712/join
2. Go to workspace settings
3. Add your integration to the team workspace
4. Grant appropriate permissions

---

## 🧪 **Test Your Setup**

After sharing the databases, test the connection:

```bash
# Test basic connection
python scripts/simple_notion_test.py

# Test full integration
python scripts/fix_notion_access.py

# If successful, run full integration
python scripts/connect_lab_centers.py
```

---

## 🔄 **Alternative: Create New Integration**

If you're having trouble with the existing integration, create a new one:

### **Step 1: Create New Integration**
1. Go to: https://www.notion.so/my-integrations
2. Click **"+ New integration"**
3. **Name**: "KP Lab Automation System"
4. **Associated workspace**: Select your workspace
5. **Capabilities**: 
   - ✅ Read content
   - ✅ Update content  
   - ✅ Insert content
6. Click **"Submit"**

### **Step 2: Get New Token**
1. Copy the **"Internal Integration Token"**
2. Update your `.env` file:
   ```bash
   NOTION_API_TOKEN_PRIMARY=your_new_token_here
   ```

### **Step 3: Share Everything with New Integration**
Follow the sharing steps above with your new integration name.

---

## 🎯 **Expected Results**

Once sharing is complete, you should see:

✅ **API Connection**: Working  
✅ **Database Access**: Working  
✅ **Page Access**: Working  
✅ **Team Workspace**: Connected  

---

## 🚨 **Troubleshooting**

### **"Could not find database" Error**
- **Cause**: Database not shared with integration
- **Fix**: Follow sharing instructions above
- **Verify**: Integration appears in database "Shared with" list

### **"Insufficient permissions" Error**  
- **Cause**: Integration has "Can view" instead of "Can edit"
- **Fix**: Update integration permissions to "Can edit"

### **Token Invalid Error**
- **Cause**: Token expired or incorrect
- **Fix**: Generate new token from https://www.notion.so/my-integrations

### **Integration Not Found Error**
- **Cause**: Integration name doesn't match
- **Fix**: Use exact integration name when sharing

---

## 🔧 **Manual Verification Steps**

1. **Check Integration Status**:
   - Go to https://www.notion.so/my-integrations
   - Verify integration is "Active"
   - Check associated workspace

2. **Verify Database Sharing**:
   - Go to each database
   - Check "Shared with" section
   - Confirm integration is listed with "Can edit" permissions

3. **Test API Access**:
   ```bash
   python scripts/simple_notion_test.py
   ```

4. **Run Full Diagnostic**:
   ```bash
   python scripts/fix_notion_access.py
   ```

---

## 🎉 **Once Everything is Working**

Run the complete integration:

```bash
python scripts/connect_lab_centers.py
```

This will:
- ✅ Connect all your lab command centers
- ✅ Set up real-time data synchronization
- ✅ Configure automated alerts
- ✅ Enable team collaboration features
- ✅ Start the monitoring system

---

## 📞 **Need Help?**

If you're still having issues:

1. **Check the logs**: `logs/lab_automation.log`
2. **Run diagnostics**: `python scripts/fix_notion_access.py`
3. **Verify all sharing steps** were completed
4. **Try creating a new integration** if problems persist

---

**🔗 Quick Links:**
- [Notion Integrations](https://www.notion.so/my-integrations)
- [Team Performance DB](https://www.notion.so/c1500b1816b14018beabe2b826ccafe9)
- [Incident Tracking DB](https://www.notion.so/cf2bb4448aff4324a602cb770cbae0a2)
- [Team Workspace](https://www.notion.so/team/1cdd2227-51b3-818e-8bb7-004288f69712/join)
