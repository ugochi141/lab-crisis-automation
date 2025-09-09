#!/usr/bin/env python3
"""Test all repositories in the workspace."""

import os
import subprocess
import json
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return output."""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, str(e)

def test_repository(repo_path):
    """Test a single repository."""
    repo_name = os.path.basename(repo_path)
    results = {
        "name": repo_name,
        "path": repo_path,
        "status": "unknown",
        "tests": []
    }
    
    # Check if directory exists
    if not os.path.exists(repo_path):
        results["status"] = "not_found"
        return results
    
    # Check git status
    success, output = run_command("git status --porcelain", repo_path)
    if success:
        results["git_status"] = "clean" if not output.strip() else "modified"
    
    # Check for Python tests
    if os.path.exists(os.path.join(repo_path, "tests")):
        success, output = run_command("python -m pytest tests/ -q", repo_path)
        results["tests"].append({
            "type": "pytest",
            "success": success,
            "message": "Tests passed" if success else "Tests failed or not found"
        })
    
    # Check for package.json (Node.js project)
    if os.path.exists(os.path.join(repo_path, "package.json")):
        success, output = run_command("npm test -- --watchAll=false", repo_path)
        results["tests"].append({
            "type": "npm",
            "success": success,
            "message": "Tests passed" if success else "No tests configured"
        })
    
    # Check for main Python files
    py_files = list(Path(repo_path).glob("*.py"))[:3]
    if py_files:
        for py_file in py_files:
            success, output = run_command(f"python -m py_compile {py_file.name}", repo_path)
            if success:
                results["tests"].append({
                    "type": "syntax",
                    "file": py_file.name,
                    "success": True,
                    "message": "Syntax valid"
                })
    
    # Determine overall status
    if results["tests"]:
        all_passed = all(t["success"] for t in results["tests"])
        results["status"] = "passing" if all_passed else "failing"
    else:
        results["status"] = "no_tests"
    
    return results

def main():
    """Test all repositories."""
    repos_to_test = [
        "/Users/ugochi141/Desktop/LabAutomation",
        "/Users/ugochi141/Critical-Values-Alert-System",
        "/Users/ugochi141/HL7-Lab-Results-Pipeline",
        "/Users/ugochi141/frontend/lab-order-dashboard-frontend",
        "/Users/ugochi141/BioPythonAssignment",
        "/Users/ugochi141/JHU_Bioinformatics_Portfolio",
        "/Users/ugochi141/huntington_analysis"
    ]
    
    print("=" * 60)
    print("TESTING ALL REPOSITORIES")
    print("=" * 60)
    
    all_results = []
    
    for repo_path in repos_to_test:
        print(f"\nTesting: {repo_path}")
        print("-" * 40)
        
        results = test_repository(repo_path)
        all_results.append(results)
        
        # Print summary
        status_emoji = {
            "passing": "✅",
            "failing": "❌",
            "no_tests": "⚠️",
            "not_found": "❓",
            "unknown": "❓"
        }
        
        print(f"Status: {status_emoji[results['status']]} {results['status'].upper()}")
        
        if results.get("git_status"):
            print(f"Git: {results['git_status']}")
        
        for test in results.get("tests", []):
            test_emoji = "✓" if test["success"] else "✗"
            print(f"  {test_emoji} {test['type']}: {test['message']}")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passing = sum(1 for r in all_results if r["status"] == "passing")
    failing = sum(1 for r in all_results if r["status"] == "failing")
    no_tests = sum(1 for r in all_results if r["status"] == "no_tests")
    not_found = sum(1 for r in all_results if r["status"] == "not_found")
    
    print(f"✅ Passing: {passing}")
    print(f"❌ Failing: {failing}")
    print(f"⚠️  No Tests: {no_tests}")
    print(f"❓ Not Found: {not_found}")
    print(f"Total: {len(all_results)}")
    
    # Save results
    with open("test_results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nDetailed results saved to test_results.json")
    
    return 0 if failing == 0 else 1

if __name__ == "__main__":
    exit(main())