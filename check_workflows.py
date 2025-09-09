#!/usr/bin/env python3
"""Check all GitHub workflows for issues."""

import yaml
import os
from pathlib import Path

def check_workflow(workflow_path):
    """Check a single workflow file."""
    print(f"\n📋 Checking: {workflow_path}")
    print("-" * 50)
    
    issues = []
    warnings = []
    
    try:
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
        
        # Check basic structure
        if not workflow:
            issues.append("Empty workflow file")
            return issues, warnings
        
        if 'name' not in workflow:
            warnings.append("No workflow name specified")
        else:
            print(f"Name: {workflow['name']}")
        
        # Check triggers
        if 'on' in workflow:
            triggers = workflow['on']
            print(f"Triggers: {', '.join(triggers.keys()) if isinstance(triggers, dict) else triggers}")
        else:
            issues.append("No triggers defined")
        
        # Check jobs
        if 'jobs' not in workflow:
            issues.append("No jobs defined")
        else:
            jobs = workflow['jobs']
            print(f"Jobs: {', '.join(jobs.keys())}")
            
            for job_name, job_config in jobs.items():
                # Check runs-on
                if 'runs-on' not in job_config:
                    issues.append(f"Job '{job_name}' missing 'runs-on'")
                
                # Check steps
                if 'steps' not in job_config:
                    issues.append(f"Job '{job_name}' has no steps")
                else:
                    steps = job_config['steps']
                    for i, step in enumerate(steps):
                        # Check for common issues
                        if 'uses' in step:
                            action = step['uses']
                            # Check for non-existent actions
                            if 'setup-powershell@' in action:
                                issues.append(f"Job '{job_name}' step {i+1}: actions/setup-powershell doesn't exist")
                        
                        if 'run' in step:
                            run_cmd = step['run']
                            # Check for script references
                            if '.ps1' in run_cmd or '.py' in run_cmd or '.js' in run_cmd:
                                # Extract script path
                                import re
                                scripts = re.findall(r'[\.\\\/]?scripts[\\\/]\S+\.\w+', run_cmd)
                                for script in scripts:
                                    script_path = script.replace('\\', '/')
                                    script_path = script_path.replace('./', '')
                                    if not os.path.exists(script_path):
                                        issues.append(f"Job '{job_name}': Script not found: {script_path}")
        
        # Check environment variables
        if 'env' in workflow:
            env_vars = workflow['env']
            secrets_used = [k for k, v in env_vars.items() if '${{ secrets.' in str(v)]
            if secrets_used:
                print(f"Secrets used: {', '.join(secrets_used)}")
        
    except yaml.YAMLError as e:
        issues.append(f"YAML syntax error: {e}")
    except Exception as e:
        issues.append(f"Error reading workflow: {e}")
    
    return issues, warnings

def main():
    """Check all workflows."""
    print("=" * 60)
    print("🔍 GITHUB WORKFLOWS CHECK")
    print("=" * 60)
    
    workflows_dir = Path(".github/workflows")
    workflow_files = list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml"))
    
    if not workflow_files:
        print("No workflow files found!")
        return 1
    
    all_issues = {}
    all_warnings = {}
    
    for workflow_file in workflow_files:
        issues, warnings = check_workflow(workflow_file)
        
        if issues:
            all_issues[workflow_file.name] = issues
        if warnings:
            all_warnings[workflow_file.name] = warnings
        
        # Print immediate status
        if issues:
            print("❌ ISSUES FOUND:")
            for issue in issues:
                print(f"  - {issue}")
        elif warnings:
            print("⚠️  WARNINGS:")
            for warning in warnings:
                print(f"  - {warning}")
        else:
            print("✅ No issues found")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    total_workflows = len(workflow_files)
    workflows_with_issues = len(all_issues)
    workflows_with_warnings = len(all_warnings)
    workflows_ok = total_workflows - workflows_with_issues
    
    print(f"Total workflows: {total_workflows}")
    print(f"✅ Passing: {workflows_ok}")
    print(f"❌ With issues: {workflows_with_issues}")
    print(f"⚠️  With warnings: {workflows_with_warnings}")
    
    if all_issues:
        print("\n🔧 FIXES NEEDED:")
        for workflow, issues in all_issues.items():
            print(f"\n{workflow}:")
            for issue in issues:
                print(f"  - {issue}")
    else:
        print("\n✅ All workflows are properly configured!")
    
    return 0 if not all_issues else 1

if __name__ == "__main__":
    exit(main())