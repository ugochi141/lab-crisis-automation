#!/bin/bash

# Lab Crisis Automation - Secure Push Script
# This script creates a clean repository and pushes it to GitHub

echo "🚀 Starting secure push to GitHub..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "📁 Initializing new git repository..."
    git init
    git branch -M main
fi

# Remove any existing remote
echo "🔗 Setting up remote repository..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/ugochi141/lab-crisis-automation.git

# Create .gitignore to prevent sensitive files
echo "🔒 Creating .gitignore for security..."
cat > .gitignore << EOF
# Environment variables
.env
*.env
.env.local
.env.production

# Logs
logs/
*.log

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.temp
*.bak
*.backup

# Sensitive data
config/lab_config.py
scripts/test_*.py
scripts/working_*.py
scripts/check_*.py
EOF

# Add all files except ignored ones
echo "📦 Adding files to git..."
git add .

# Check for any remaining secrets
echo "🔍 Checking for secrets..."
if grep -r "secret_" . --exclude-dir=.git --exclude="*.md" --exclude="push_to_github.sh" --exclude=".gitignore"; then
    echo "❌ Found secrets in files! Please remove them before pushing."
    exit 1
fi

# Commit changes
echo "💾 Committing changes..."
git commit -m "🔒 Secure Lab Crisis Automation System

✅ Security Features:
- Environment variable configuration
- No hardcoded credentials
- GitHub Secrets integration
- Secure configuration management

🚀 Automation Features:
- Real-time crisis monitoring
- Automated Teams alerts
- Notion database integration
- Power BI data streaming
- GitHub Actions workflow
- Mobile command center

📊 Crisis Management:
- TAT Compliance monitoring
- Wait time alerts
- Staffing gap tracking
- Performance analytics
- Incident management

Ready for production deployment! 🚀"

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed to GitHub!"
    echo "🌐 Repository: https://github.com/ugochi141/lab-crisis-automation"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Go to GitHub repository settings"
    echo "2. Add your secrets in Settings > Secrets and variables > Actions"
    echo "3. Enable GitHub Actions workflow"
    echo "4. Test the system with: python scripts/secure_crisis_monitor.py"
else
    echo "❌ Push failed. Please check the error messages above."
    echo "💡 Try running: git status"
fi
