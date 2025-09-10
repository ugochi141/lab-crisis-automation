# 🚀 Quick Deploy: Get Your Webhook Online in 5 Minutes

## Option 1: Railway (Free & Fast)

### Step 1: Deploy to Railway
1. **Visit**: https://railway.app
2. **Sign up** with your GitHub account (free)
3. **Click "Deploy from GitHub repo"**
4. **Select your LabAutomation repository**

### Step 2: Set Environment Variables
In Railway dashboard, go to **Variables** tab and add:

```
NOTION_API_TOKEN_PRIMARY=your_notion_api_token_here
NOTION_VERSION=2022-06-28
NOTION_PERFORMANCE_DB_ID=your_performance_db_id_here
NOTION_INCIDENT_DB_ID=your_incident_db_id_here
NOTION_WEBHOOK_SECRET=webhook_secret_12345
FLASK_ENV=production
```

### Step 3: Get Your URL
Railway will give you a URL like: `https://labautomation-production.up.railway.app`

**Your webhook endpoint**: `https://your-app.railway.app/webhook/notion`

---

## Option 2: Render (Also Free)

### Step 1: Deploy to Render
1. **Visit**: https://render.com
2. **Sign up** with GitHub
3. **Create Web Service**
4. **Connect your GitHub repo**

### Step 2: Configure Service
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python main.py`
- **Environment**: Add the same variables as above

### Step 3: Get Your URL
Render gives you: `https://your-app.onrender.com`

**Your webhook endpoint**: `https://your-app.onrender.com/webhook/notion`

---

## 📋 Next: Configure in Notion

Once you have your public URL:

### Step 1: Go to Notion
1. **Visit**: https://www.notion.so
2. **Settings & Members** → **Integrations** → **Webhooks**
3. **Click "Add webhook"**

### Step 2: Configure Webhook
- **Name**: Lab Automation System
- **Endpoint URL**: `https://your-app.railway.app/webhook/notion`
- **Secret**: `webhook_secret_12345`
- **Events**: Select:
  - ✅ `page.updated`
  - ✅ `database.updated`
  - ✅ `page.created`

### Step 3: Select Databases
Choose your databases:
- ✅ Performance Database
- ✅ Incident Database

### Step 4: Save & Verify
Click "Create webhook" - Notion will automatically verify!

## ✅ Success Indicators

**In Notion**: Webhook shows "Verified" ✅
**Test URL**: `curl https://your-app.railway.app/health`

## 🎉 You're Live!

Your webhook is now:
- ✅ Publicly accessible
- ✅ Verified by Notion  
- ✅ Monitoring your databases
- ✅ Ready for real-time automation

**Next**: Test by editing a record in your Notion database!