# Deployment Guide for Notion Webhook Server

## 🚀 Quick Start: Testing with ngrok

**Best for: Initial testing and development**

### Prerequisites
1. Your webhook server is running locally on port 8080
2. You have an ngrok account (free tier available)

### Steps
1. **Get ngrok auth token**: Visit https://dashboard.ngrok.com/get-started/your-authtoken
2. **Configure ngrok**: `ngrok config add-authtoken YOUR_TOKEN`
3. **Start tunnel**: `./scripts/start_ngrok_tunnel.sh`
4. **Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`)
5. **Use in Notion**: `https://abc123.ngrok.io/webhook/notion`

✅ **Pros**: Instant, no deployment needed  
❌ **Cons**: Temporary URL, requires local server running

---

## ☁️ Production Deployment Options

### Option 1: Railway (Recommended)

**Best for: Simple, fast deployment with automatic HTTPS**

1. **Create account**: https://railway.app
2. **Connect GitHub repo** with your LabAutomation code
3. **Set environment variables** in Railway dashboard:
   ```
   NOTION_API_TOKEN_PRIMARY=your_token
   NOTION_PERFORMANCE_DB_ID=your_db_id
   NOTION_INCIDENT_DB_ID=your_db_id
   NOTION_WEBHOOK_SECRET=webhook_secret_12345
   ```
4. **Deploy**: Railway auto-deploys from Git
5. **Get URL**: Railway provides https://your-app.railway.app

**Cost**: Free tier available, $5/month for production

### Option 2: Render

**Best for: Free hosting with automatic SSL**

1. **Create account**: https://render.com
2. **Create Web Service** from GitHub repo
3. **Use settings** from `deployments/render.yaml`
4. **Set environment variables** in Render dashboard
5. **Deploy**: Automatic from Git pushes

**Cost**: Free tier available (with limitations)

### Option 3: Heroku

**Best for: Enterprise-grade with extensive add-ons**

1. **Install Heroku CLI**: `brew install heroku/brew/heroku`
2. **Login**: `heroku login`
3. **Create app**: `heroku create notion-webhook-lab`
4. **Set environment variables**:
   ```bash
   heroku config:set NOTION_API_TOKEN_PRIMARY=your_token
   heroku config:set NOTION_PERFORMANCE_DB_ID=your_db_id
   heroku config:set NOTION_INCIDENT_DB_ID=your_db_id
   heroku config:set NOTION_WEBHOOK_SECRET=webhook_secret_12345
   ```
5. **Copy Procfile**: `cp deployments/Procfile .`
6. **Deploy**: `git push heroku main`

**Cost**: $7/month minimum for production apps

### Option 4: AWS Lambda (Serverless)

**Best for: High scale, pay-per-request**

1. **Install Serverless Framework**: `npm install -g serverless`
2. **Create serverless.yml** configuration
3. **Deploy**: `serverless deploy`
4. **Configure API Gateway** for webhook endpoint

**Cost**: Pay per request, very cost-effective for low traffic

---

## 🔧 Configuration for Production

### Required Environment Variables
```bash
# Notion API
NOTION_API_TOKEN_PRIMARY=ntn_...
NOTION_VERSION=2022-06-28
NOTION_PERFORMANCE_DB_ID=c1500b18...
NOTION_INCIDENT_DB_ID=cf2bb444...

# Webhook
WEBHOOK_PORT=8080
NOTION_WEBHOOK_SECRET=webhook_secret_12345

# Production
FLASK_ENV=production
```

### Update webhook server for production

Edit `scripts/notion_webhook_server.py` to use PORT from environment:

```python
if __name__ == '__main__':
    port = int(os.getenv('PORT', os.getenv('WEBHOOK_PORT', 8080)))
    app.run(host='0.0.0.0', port=port)
```

---

## 📋 Final Steps: Configure Notion Webhook

Once you have a public URL:

1. **Go to Notion**: https://www.notion.so
2. **Settings & Members** → **Integrations** → **Webhooks**
3. **Add webhook**:
   - **URL**: `https://your-domain.com/webhook/notion`
   - **Secret**: `webhook_secret_12345`
   - **Events**: Select relevant events:
     - ✅ `page.updated` (for performance tracking)
     - ✅ `database.updated` (for incident management)

4. **Test verification**: Notion will send a challenge request
5. **Check logs**: Your server should respond with the challenge

---

## ✅ Verification Success

You'll know verification worked when:
- ✅ Notion shows "Verified" status
- ✅ Your server logs show challenge received/responded
- ✅ Test events start flowing to your webhook

**Your lab automation system will now receive real-time updates from Notion! 🎉**