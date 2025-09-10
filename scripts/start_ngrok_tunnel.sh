#!/bin/bash

# Start ngrok tunnel script
echo "🚀 Starting ngrok tunnel for Notion webhook..."

# Check if webhook server is running
if ! curl -s http://localhost:8080/health > /dev/null; then
    echo "❌ Webhook server is not running on port 8080"
    echo "Start it first with: python scripts/notion_webhook_server.py"
    exit 1
fi

echo "✅ Webhook server is running"
echo "🔗 Starting ngrok tunnel..."

# Start ngrok tunnel
ngrok http 8080 --log stdout

# Note: The ngrok URL will be displayed in the terminal
# Use that URL + /webhook/notion as your Notion webhook endpoint