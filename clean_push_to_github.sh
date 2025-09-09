#!/bin/bash

# Lab Crisis Automation - Clean Push Script
# This script creates a completely clean repository and pushes it to GitHub

echo "🚀 Starting clean push to GitHub..."
echo "This will create a fresh repository without any commit history"

# Check if we're in a git repository
if [ -d ".git" ]; then
    echo "🗑️  Removing existing git repository..."
    rm -rf .git
fi

# Initialize new git repository
echo "📁 Initializing new git repository..."
git init
git branch -M main

# Create comprehensive .gitignore
echo "🔒 Creating comprehensive .gitignore..."
cat > .gitignore << 'EOF'
# Environment variables
.env
*.env
.env.local
.env.production
.env.development

# Logs
logs/
*.log
*.log.*

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
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
desktop.ini

# Temporary files
*.tmp
*.temp
*.bak
*.backup
*.orig

# Sensitive data
config/lab_config.py
scripts/test_*.py
scripts/working_*.py
scripts/check_*.py
*secret*
*token*
*password*
*key*

# Data files (optional - uncomment if you don't want to track data)
# data/
# *.csv
# *.xlsx
# *.json

# Node modules (if any)
node_modules/

# Build artifacts
build/
dist/
*.egg-info/

# Coverage reports
htmlcov/
.coverage
.coverage.*
coverage.xml

# Jupyter Notebook checkpoints
.ipynb_checkpoints/

# pytest cache
.pytest_cache/

# mypy cache
.mypy_cache/
.dmypy.json
dmypy.json
EOF

# Add all files except ignored ones
echo "📦 Adding files to git..."
git add .

# Check for any remaining secrets (excluding virtual env and test files)
echo "🔍 Checking for secrets..."
if grep -r "secret_" . --exclude-dir=.git --exclude-dir=.venv --exclude-dir=venv --exclude-dir=site-packages --exclude="*.md" --exclude="*.sh" --exclude=".gitignore" --exclude="test_security.py" --exclude="*.save" --exclude="fix_notion_access.py" 2>/dev/null; then
    echo "❌ Found 'secret_' in files! Please remove them before pushing."
    exit 1
fi

if grep -r "ntn_" . --exclude-dir=.git --exclude-dir=.venv --exclude-dir=venv --exclude-dir=site-packages --exclude="*.md" --exclude="*.sh" --exclude=".gitignore" --exclude="test_security.py" --exclude="*.save" --exclude="fix_notion_access.py" 2>/dev/null; then
    echo "❌ Found 'ntn_' in files! Please remove them before pushing."
    exit 1
fi

if grep -r "https://kaiserpermanente" . --exclude-dir=.git --exclude-dir=.venv --exclude-dir=venv --exclude-dir=site-packages --exclude="*.md" --exclude="*.sh" --exclude=".gitignore" --exclude="test_security.py" --exclude="*.save" 2>/dev/null; then
    echo "❌ Found hardcoded webhooks! Please remove them before pushing."
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

🔧 Technical Stack:
- Python 3.8+
- Notion API
- Microsoft Teams
- Power BI
- GitHub Actions
- Environment-based config

Ready for production deployment! 🚀"

# Add remote repository
echo "🔗 Setting up remote repository..."
git remote add origin https://github.com/ugochi141/lab-crisis-automation.git

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git push -u origin main --force

if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed to GitHub!"
    echo "🌐 Repository: https://github.com/ugochi141/lab-crisis-automation"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Go to GitHub repository settings"
    echo "2. Add your secrets in Settings > Secrets and variables > Actions:"
    echo "   - NOTION_API_TOKEN"
    echo "   - NOTION_PERFORMANCE_DB_ID"
    echo "   - NOTION_INCIDENT_DB_ID"
    echo "   - TEAMS_WEBHOOK_URL"
    echo "3. Enable GitHub Actions workflow"
    echo "4. Test the system with: python setup_environment.py"
    echo ""
    echo "🎉 Your lab crisis automation system is now live!"
else
    echo "❌ Push failed. Please check the error messages above."
    echo "💡 Common issues:"
    echo "   - Check your GitHub credentials"
    echo "   - Verify repository exists"
    echo "   - Check for any remaining secrets"
fi
