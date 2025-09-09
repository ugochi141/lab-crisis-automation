#!/usr/bin/env python3
"""
Security Test Script
Checks that all files are using environment variables instead of hardcoded secrets
"""

import os
import re
from pathlib import Path

def check_file_security(file_path):
    """Check if a file contains hardcoded secrets"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Patterns to check for
        secret_patterns = [
            r'ntn_[a-zA-Z0-9]+',
            r'secret_[a-zA-Z0-9]+',
            r'https://kaiserpermanente\.webhook\.office\.com',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
            r'webhook\s*=\s*["\'][^"\']+["\']'
        ]
        
        issues = []
        for pattern in secret_patterns:
            matches = re.findall(pattern, content)
            if matches:
                issues.extend(matches)
        
        return issues
        
    except Exception as e:
        return [f"Error reading file: {e}"]

def main():
    """Main security check function"""
    print("🔒 Lab Crisis Automation - Security Check")
    print("=" * 50)
    
    # Files to check
    python_files = list(Path('.').rglob('*.py'))
    shell_files = list(Path('.').rglob('*.sh'))
    config_files = list(Path('.').rglob('*.json'))
    
    all_files = python_files + shell_files + config_files
    
    # Exclude certain files and directories
    exclude_patterns = [
        'test_security.py',
        'setup_environment.py',
        '.git/',
        '__pycache__/',
        'venv/',
        '.venv/',
        'site-packages/',
        '.pyc',
        '.save'
    ]
    
    files_to_check = []
    for file_path in all_files:
        should_exclude = False
        for pattern in exclude_patterns:
            if pattern in str(file_path):
                should_exclude = True
                break
        if not should_exclude:
            files_to_check.append(file_path)
    
    print(f"📁 Checking {len(files_to_check)} files...")
    print()
    
    total_issues = 0
    files_with_issues = 0
    
    for file_path in files_to_check:
        issues = check_file_security(file_path)
        if issues:
            files_with_issues += 1
            total_issues += len(issues)
            print(f"❌ {file_path}")
            for issue in issues:
                print(f"   - {issue}")
            print()
    
    print("=" * 50)
    print("📊 Security Check Summary")
    print("=" * 50)
    
    if total_issues == 0:
        print("✅ All files are secure!")
        print("🔒 No hardcoded secrets found")
        print("🚀 Ready for GitHub push!")
        return True
    else:
        print(f"❌ Found {total_issues} security issues in {files_with_issues} files")
        print("🔧 Please fix these issues before pushing to GitHub")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
