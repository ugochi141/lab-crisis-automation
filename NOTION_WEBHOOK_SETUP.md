# Notion Webhook Setup Guide

## ✅ Current Status
Your webhook verification server is **running and ready** on port 8080!

## 🔧 Server Details
- **Health Check**: http://localhost:8080/health
- **Verification Endpoint**: http://localhost:8080/webhook/notion/verify  
- **Main Webhook**: http://localhost:8080/webhook/notion
- **Status**: ✅ Running and tested

## 📋 Next Steps to Complete Verification

### Option 1: Local Testing with ngrok (Recommended for testing)
1. **Install ngrok**: `brew install ngrok` (or download from ngrok.com)
2. **Expose your local server**: 
   ```bash
   ngrok http 8080
   ```
3. **Copy the ngrok URL** (e.g., `https://abc123.ngrok.io`)
4. **Use this URL in Notion**: `https://abc123.ngrok.io/webhook/notion`

### Option 2: Production Deployment
Deploy the webhook server to a cloud service:
- **Heroku**: Simple deployment with Git
- **Railway**: One-click deployment
- **Render**: Free tier available
- **AWS Lambda**: Serverless option

## 🔐 Notion Webhook Configuration

1. **Go to Notion**: https://www.notion.so
2. **Settings & Members** → **Integrations** → **Webhooks**
3. **Add webhook** with these settings:
   - **Endpoint URL**: `https://your-domain.com/webhook/notion`
   - **Secret**: `webhook_secret_12345` (already configured)
   - **Events**: Select events you want to monitor:
     - ✅ Page updated (for performance data changes)
     - ✅ Database updated (for incident management)

## 🧪 Test Verification

Once you have a public URL, test the verification:

```bash
curl -X POST https://your-domain.com/webhook/notion/verify \
  -H "Content-Type: application/json" \
  -d '{"challenge": "test_123"}'
```

**Expected Response**: `{"challenge": "test_123"}`

## 🚀 What Happens After Verification

Once verified, your webhook will receive events when:
- Performance database records are updated
- Incident database records are created/updated
- Any monitored pages or databases change

The server will:
1. ✅ Verify the webhook signature
2. ✅ Process the event data
3. ✅ Trigger appropriate lab automation responses
4. ✅ Log all activities for audit

## 📝 Current Environment Variables
```
WEBHOOK_PORT=8080
NOTION_WEBHOOK_SECRET=webhook_secret_12345
NOTION_API_TOKEN_PRIMARY=[configured]
NOTION_PERFORMANCE_DB_ID=[configured]
NOTION_INCIDENT_DB_ID=[configured]
```

## 🔄 Server Commands
- **Start**: `python scripts/notion_webhook_server.py`
- **Health Check**: `curl http://localhost:8080/health`
- **Stop**: Press Ctrl+C

---

**Your webhook server is ready for verification! 🎉**