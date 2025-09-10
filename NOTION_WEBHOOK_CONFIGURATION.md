# 📋 Step-by-Step: Configure Notion Webhook

## 🎯 Current Status
- ✅ Webhook server is running on port 8080
- ✅ Verification endpoint is ready
- ✅ All deployment options are prepared

## 🚀 Choose Your Deployment Method

### Method 1: Quick Testing with ngrok (5 minutes)

**Step 1: Get ngrok token**
1. Visit: https://dashboard.ngrok.com/get-started/your-authtoken
2. Sign up (free) and copy your auth token
3. Run: `ngrok config add-authtoken YOUR_TOKEN`

**Step 2: Start ngrok tunnel**
```bash
# Make sure your webhook server is running
./scripts/start_ngrok_tunnel.sh
```

**Step 3: Copy the HTTPS URL**
- ngrok will show: `https://abc123.ngrok.io -> http://localhost:8080`
- Copy the `https://abc123.ngrok.io` part

### Method 2: Production with Railway (10 minutes)

**Step 1: Create Railway account**
1. Go to: https://railway.app
2. Sign up with GitHub

**Step 2: Deploy from GitHub**
1. Connect your GitHub repository
2. Select "Deploy from GitHub repo"
3. Choose your LabAutomation repository

**Step 3: Set environment variables**
In Railway dashboard, add these variables:
```
NOTION_API_TOKEN_PRIMARY=your_notion_api_token_here
NOTION_PERFORMANCE_DB_ID=your_performance_db_id_here
NOTION_INCIDENT_DB_ID=your_incident_db_id_here
NOTION_WEBHOOK_SECRET=webhook_secret_12345
FLASK_ENV=production
```

**Step 4: Get your Railway URL**
- Railway will provide: `https://your-app.railway.app`

---

## 🔗 Configure Webhook in Notion

**Step 1: Access Notion Settings**
1. Open Notion in browser: https://www.notion.so
2. Click your workspace name (top left)
3. Go to "Settings & Members"

**Step 2: Navigate to Webhooks**
1. In the left sidebar, click "Integrations"
2. Click "Webhooks" 
3. Click "Add webhook"

**Step 3: Configure Webhook**
Fill in these details:

- **Name**: `Lab Automation System`
- **Endpoint URL**: 
  - For ngrok: `https://abc123.ngrok.io/webhook/notion`
  - For Railway: `https://your-app.railway.app/webhook/notion`
- **Secret**: `webhook_secret_12345`
- **Events**: Select these events:
  - ✅ `page.updated` (when performance data changes)
  - ✅ `database.updated` (when incident records change)
  - ✅ `page.created` (for new incidents)

**Step 4: Select Databases**
Choose which databases to monitor:
- ✅ Performance Database (c1500b18...)
- ✅ Incident Database (cf2bb444...)

**Step 5: Save and Verify**
1. Click "Create webhook"
2. Notion will immediately send a verification challenge
3. Your webhook server will automatically respond

## ✅ Verification Success Indicators

You'll know it worked when you see:

**In Notion:**
- ✅ Webhook status shows "Verified"
- ✅ Green checkmark next to your webhook

**In Your Server Logs:**
```
INFO:__main__:Handling URL verification challenge
INFO:__main__:Responding to challenge: challenge_12345...
```

**Test Health Check:**
```bash
curl https://your-webhook-url/health
# Should return: {"status":"healthy",...}
```

## 🧪 Test Your Webhook

**Step 1: Make a change in Notion**
1. Go to your Performance Database
2. Edit any record (add a note, change a number)
3. Save the change

**Step 2: Check webhook logs**
You should see:
```
INFO:__main__:Processing webhook event: page.updated
INFO:__main__:Page updated: 12345...
```

**Step 3: Teams notification (if configured)**
Your Teams channel should receive notifications about the database changes.

## 🔧 Troubleshooting

**Webhook shows "Failed":**
- Check your server is running and accessible
- Verify the URL is correct (include `/webhook/notion`)
- Ensure HTTPS is used (not HTTP)

**No events received:**
- Check you selected the right databases
- Verify events are enabled (page.updated, etc.)
- Test with a simple page edit

**400 Bad Request:**
- Check webhook secret matches
- Verify JSON payload structure
- Look at server error logs

## 🎉 You're Done!

Your Notion webhook is now:
- ✅ Verified and active
- ✅ Monitoring your lab databases
- ✅ Ready to trigger automation workflows
- ✅ Sending real-time updates to your system

**Next steps:**
- Monitor webhook logs for incoming events
- Customize event processing in your server
- Add Teams notifications for critical alerts
- Set up dashboard updates for performance metrics