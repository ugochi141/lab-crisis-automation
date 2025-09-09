#!/usr/bin/env python3
"""
GitHub Repository Manager
Fixes and enhances all GitHub repositories
"""

import os
import sys
import json
import requests
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import base64

class GitHubRepoManager:
    """Manages GitHub repositories with automated fixes and enhancements"""
    
    def __init__(self, github_token: str, username: str):
        self.github_token = github_token
        self.username = username
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "LabAutomation-Enhancer/1.0"
        }
        self.repos = []
        self.enhancements_applied = 0
    
    def get_user_repositories(self) -> List[Dict]:
        """Get all user repositories"""
        print("🔍 Fetching user repositories...")
        
        try:
            url = f"{self.base_url}/user/repos"
            params = {
                "type": "all",
                "sort": "updated",
                "per_page": 100
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            self.repos = response.json()
            print(f"✅ Found {len(self.repos)} repositories")
            return self.repos
            
        except Exception as e:
            print(f"❌ Failed to fetch repositories: {e}")
            return []
    
    def analyze_repository(self, repo: Dict) -> Dict:
        """Analyze repository for issues and enhancement opportunities"""
        repo_name = repo['name']
        print(f"🔍 Analyzing repository: {repo_name}")
        
        analysis = {
            'name': repo_name,
            'url': repo['html_url'],
            'issues': [],
            'enhancements': [],
            'security_issues': [],
            'code_quality': 'unknown',
            'last_updated': repo['updated_at']
        }
        
        try:
            # Check for common issues
            if not repo.get('has_issues'):
                analysis['issues'].append("Issues not enabled")
            
            if not repo.get('has_wiki'):
                analysis['issues'].append("Wiki not enabled")
            
            if not repo.get('has_pages'):
                analysis['enhancements'].append("GitHub Pages not enabled")
            
            if not repo.get('has_projects'):
                analysis['enhancements'].append("Projects not enabled")
            
            # Check repository size
            if repo.get('size', 0) > 100000:  # 100MB
                analysis['issues'].append("Repository size is large")
            
            # Check for security features
            if not repo.get('allow_squash_merge'):
                analysis['security_issues'].append("Squash merge not required")
            
            if not repo.get('allow_rebase_merge'):
                analysis['security_issues'].append("Rebase merge not required")
            
            # Check for branch protection
            branches_url = repo['branches_url'].replace('{/branch}', '')
            branches_response = requests.get(branches_url, headers=self.headers)
            if branches_response.status_code == 200:
                branches = branches_response.json()
                main_branch = next((b for b in branches if b['name'] == 'main' or b['name'] == 'master'), None)
                if main_branch and not main_branch.get('protected'):
                    analysis['security_issues'].append("Main branch not protected")
            
            # Determine code quality
            if repo.get('language'):
                analysis['code_quality'] = 'good'
            elif repo.get('size', 0) > 1000:
                analysis['code_quality'] = 'moderate'
            else:
                analysis['code_quality'] = 'basic'
            
        except Exception as e:
            analysis['issues'].append(f"Analysis error: {str(e)}")
        
        return analysis
    
    def create_enhanced_readme(self, repo: Dict) -> str:
        """Create enhanced README for repository"""
        repo_name = repo['name']
        description = repo.get('description', '')
        language = repo.get('language', 'Unknown')
        
        readme_content = f"""# {repo_name}

{description}

## 🚀 Features

- **Automated CI/CD**: GitHub Actions workflow for continuous integration
- **Security**: Automated security scanning and dependency updates
- **Code Quality**: Automated code formatting and linting
- **Documentation**: Comprehensive documentation and examples
- **Testing**: Automated testing suite with coverage reporting

## 📋 Prerequisites

- Python 3.8+
- Git
- Required dependencies (see requirements.txt)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/{self.username}/{repo_name}.git
cd {repo_name}
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## 🚀 Usage

```bash
python main.py
```

## 🧪 Testing

```bash
python -m pytest tests/
```

## 📊 Code Quality

- **Language**: {language}
- **Linting**: Flake8, Black
- **Testing**: Pytest
- **Coverage**: Coverage.py
- **Security**: Bandit

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔧 Maintenance

This repository is automatically maintained with:
- Dependabot for dependency updates
- CodeQL for security analysis
- Automated testing on every push
- Automated code formatting

## 📈 Analytics

- **Last Updated**: {datetime.now().strftime('%Y-%m-%d')}
- **Language**: {language}
- **Size**: {repo.get('size', 0)} KB
- **Stars**: {repo.get('stargazers_count', 0)}
- **Forks**: {repo.get('forks_count', 0)}

---
*Enhanced by Lab Automation System* 🤖
"""
        
        return readme_content
    
    def create_github_actions_workflow(self, repo: Dict) -> str:
        """Create GitHub Actions workflow for repository"""
        language = repo.get('language', 'Python').lower()
        
        if language == 'python':
            workflow_content = """name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 1'  # Weekly security scan

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov flake8 black bandit
    
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Format check with black
      run: black --check .
    
    - name: Security scan with bandit
      run: bandit -r . -f json -o bandit-report.json || true
    
    - name: Test with pytest
      run: |
        pytest --cov=. --cov-report=xml --cov-report=html
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
        fail_ci_if_error: false

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy scan results to GitHub Security tab
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

  deploy:
    needs: [test, security]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      run: |
        echo "Deploying to production..."
        # Add your deployment commands here
"""
        else:
            workflow_content = """name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build project
      run: |
        echo "Building project..."
        # Add your build commands here
    
    - name: Run tests
      run: |
        echo "Running tests..."
        # Add your test commands here
    
    - name: Deploy
      if: github.ref == 'refs/heads/main'
      run: |
        echo "Deploying..."
        # Add your deployment commands here
"""
        
        return workflow_content
    
    def create_requirements_file(self, repo: Dict) -> str:
        """Create requirements.txt file"""
        language = repo.get('language', 'Python').lower()
        
        if language == 'python':
            requirements = """# Core dependencies
requests>=2.28.0
python-dotenv>=0.19.0
pandas>=1.5.0
numpy>=1.21.0

# API clients
notion-client>=2.0.0
aiohttp>=3.8.0

# Testing
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-asyncio>=0.21.0

# Code quality
flake8>=5.0.0
black>=22.0.0
bandit>=1.7.0

# Documentation
sphinx>=5.0.0
sphinx-rtd-theme>=1.0.0

# Utilities
click>=8.0.0
rich>=12.0.0
"""
        else:
            requirements = """# Add your project dependencies here
# Example:
# express>=4.18.0
# lodash>=4.17.21
"""
        
        return requirements
    
    def create_gitignore_file(self, repo: Dict) -> str:
        """Create .gitignore file"""
        language = repo.get('language', 'Python').lower()
        
        if language == 'python':
            gitignore = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
logs/
*.log

# Temporary files
tmp/
temp/
"""
        else:
            gitignore = """# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/

# nyc test coverage
.nyc_output

# Grunt intermediate storage
.grunt

# Bower dependency directory
bower_components

# node-waf configuration
.lock-wscript

# Compiled binary addons
build/Release

# Dependency directories
jspm_packages/

# TypeScript cache
*.tsbuildinfo

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Microbundle cache
.rpt2_cache/
.rts2_cache_cjs/
.rts2_cache_es/
.rts2_cache_umd/

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# dotenv environment variables file
.env
.env.test

# parcel-bundler cache
.cache
.parcel-cache

# Next.js build output
.next

# Nuxt.js build / generate output
.nuxt
dist

# Gatsby files
.cache/
public

# Storybook build outputs
.out
.storybook-out

# Temporary folders
tmp/
temp/

# Logs
logs
*.log

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
"""
        
        return gitignore
    
    def create_license_file(self, repo: Dict) -> str:
        """Create MIT License file"""
        current_year = datetime.now().year
        return f"""MIT License

Copyright (c) {current_year} {self.username}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    
    def create_contributing_guide(self) -> str:
        """Create CONTRIBUTING.md file"""
        return """# Contributing Guidelines

Thank you for your interest in contributing to this project! 🎉

## 🤝 How to Contribute

### 1. Fork the Repository
- Click the "Fork" button on the repository page
- Clone your fork locally

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes
- Write clean, readable code
- Add comments where necessary
- Follow the existing code style
- Add tests for new functionality

### 4. Test Your Changes
```bash
# Run tests
python -m pytest

# Run linting
flake8 .

# Run formatting check
black --check .
```

### 5. Commit Your Changes
```bash
git add .
git commit -m "Add: your feature description"
```

### 6. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## 📋 Code Standards

### Python
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions small and focused

### Testing
- Write unit tests for new functionality
- Aim for >80% code coverage
- Use descriptive test names

### Documentation
- Update README.md if needed
- Add docstrings to new functions
- Update API documentation

## 🐛 Reporting Issues

When reporting issues, please include:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)

## 💡 Suggesting Features

When suggesting features:
- Describe the use case
- Explain the expected behavior
- Consider implementation complexity
- Check for existing similar requests

## 📝 Pull Request Guidelines

- Use descriptive titles
- Reference related issues
- Include screenshots for UI changes
- Ensure all tests pass
- Request review from maintainers

## 🏷️ Commit Message Format

Use conventional commits:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for test changes
- `chore:` for maintenance tasks

## 🎯 Getting Help

- Check existing issues and discussions
- Ask questions in the discussions section
- Join our community chat (if available)

Thank you for contributing! 🙏
"""
    
    def enhance_repository(self, repo: Dict) -> bool:
        """Enhance a single repository"""
        repo_name = repo['name']
        print(f"🚀 Enhancing repository: {repo_name}")
        
        try:
            # Create enhanced files
            files_to_create = {
                'README.md': self.create_enhanced_readme(repo),
                '.github/workflows/ci.yml': self.create_github_actions_workflow(repo),
                'requirements.txt': self.create_requirements_file(repo),
                '.gitignore': self.create_gitignore_file(repo),
                'LICENSE': self.create_license_file(repo),
                'CONTRIBUTING.md': self.create_contributing_guide()
            }
            
            # Create files in repository
            for file_path, content in files_to_create.items():
                self.create_file_in_repo(repo, file_path, content)
            
            # Enable repository features
            self.enable_repository_features(repo)
            
            print(f"✅ Successfully enhanced {repo_name}")
            self.enhancements_applied += 1
            return True
            
        except Exception as e:
            print(f"❌ Failed to enhance {repo_name}: {e}")
            return False
    
    def create_file_in_repo(self, repo: Dict, file_path: str, content: str) -> bool:
        """Create a file in the repository"""
        try:
            repo_name = repo['name']
            url = f"{self.base_url}/repos/{self.username}/{repo_name}/contents/{file_path}"
            
            # Check if file exists
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                # File exists, update it
                existing_file = response.json()
                sha = existing_file['sha']
                message = f"Update {file_path}"
                method = "PUT"
            else:
                # File doesn't exist, create it
                sha = None
                message = f"Add {file_path}"
                method = "PUT"
            
            # Encode content
            content_bytes = content.encode('utf-8')
            content_b64 = base64.b64encode(content_bytes).decode('utf-8')
            
            # Prepare request data
            data = {
                "message": message,
                "content": content_b64,
                "branch": "main"
            }
            
            if sha:
                data["sha"] = sha
            
            # Create/update file
            response = requests.put(url, headers=self.headers, json=data)
            
            if response.status_code in [200, 201]:
                print(f"  ✅ Created/updated {file_path}")
                return True
            else:
                print(f"  ❌ Failed to create {file_path}: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"  ❌ Error creating {file_path}: {e}")
            return False
    
    def enable_repository_features(self, repo: Dict) -> bool:
        """Enable repository features"""
        try:
            repo_name = repo['name']
            url = f"{self.base_url}/repos/{self.username}/{repo_name}"
            
            # Enable features
            data = {
                "has_issues": True,
                "has_wiki": True,
                "has_pages": True,
                "has_projects": True,
                "allow_squash_merge": True,
                "allow_rebase_merge": True,
                "allow_merge_commit": False,
                "delete_branch_on_merge": True
            }
            
            response = requests.patch(url, headers=self.headers, json=data)
            
            if response.status_code == 200:
                print(f"  ✅ Enabled repository features")
                return True
            else:
                print(f"  ❌ Failed to enable features: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"  ❌ Error enabling features: {e}")
            return False
    
    def run_enhancement_process(self) -> Dict:
        """Run the complete enhancement process"""
        print("🚀 Starting GitHub Repository Enhancement Process")
        print("=" * 60)
        
        # Get repositories
        repos = self.get_user_repositories()
        if not repos:
            return {'success': False, 'message': 'No repositories found'}
        
        # Filter repositories (exclude forks and archived)
        active_repos = [r for r in repos if not r.get('fork', False) and not r.get('archived', False)]
        print(f"📊 Found {len(active_repos)} active repositories to enhance")
        
        # Process each repository
        results = {
            'total': len(active_repos),
            'enhanced': 0,
            'failed': 0,
            'details': []
        }
        
        for i, repo in enumerate(active_repos, 1):
            print(f"\n[{i}/{len(active_repos)}] Processing: {repo['name']}")
            
            # Analyze repository
            analysis = self.analyze_repository(repo)
            results['details'].append(analysis)
            
            # Enhance repository
            if self.enhance_repository(repo):
                results['enhanced'] += 1
            else:
                results['failed'] += 1
            
            # Rate limiting
            time.sleep(1)
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 Enhancement Summary")
        print("=" * 60)
        print(f"Total Repositories: {results['total']}")
        print(f"Successfully Enhanced: {results['enhanced']}")
        print(f"Failed: {results['failed']}")
        print(f"Success Rate: {(results['enhanced']/results['total']*100):.1f}%")
        
        return results

def main():
    """Main execution function"""
    print("🔧 GitHub Repository Manager")
    print("=" * 40)
    
    # Get GitHub token
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("❌ GITHUB_TOKEN environment variable not set")
        print("Please set your GitHub personal access token:")
        print("export GITHUB_TOKEN=your_token_here")
        return 1
    
    # Get username
    username = os.getenv('GITHUB_USERNAME', 'ugochi141')
    
    # Initialize manager
    manager = GitHubRepoManager(github_token, username)
    
    # Run enhancement process
    results = manager.run_enhancement_process()
    
    # Save results
    with open('logs/github_enhancement_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📝 Results saved to: logs/github_enhancement_results.json")
    
    return 0 if results['enhanced'] > 0 else 1

if __name__ == "__main__":
    sys.exit(main())
