#!/usr/bin/env python3
"""
Enhanced Repository Analysis
Comprehensive analysis of all lab repositories
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RepositoryAnalyzer:
    """Analyze all repositories comprehensively"""
    
    def __init__(self):
        self.repos = [
            {
                "name": "LabAutomation",
                "path": "/Users/ugochi141/Desktop/LabAutomation",
                "type": "main",
                "language": "python"
            },
            {
                "name": "Critical-Values-Alert-System",
                "path": "/Users/ugochi141/Critical-Values-Alert-System",
                "type": "monitoring",
                "language": "python"
            },
            {
                "name": "HL7-Lab-Results-Pipeline",
                "path": "/Users/ugochi141/HL7-Lab-Results-Pipeline",
                "type": "integration",
                "language": "python"
            },
            {
                "name": "lab-order-dashboard-frontend",
                "path": "/Users/ugochi141/frontend/lab-order-dashboard-frontend",
                "type": "frontend",
                "language": "javascript"
            },
            {
                "name": "BioPythonAssignment",
                "path": "/Users/ugochi141/BioPythonAssignment",
                "type": "academic",
                "language": "python"
            },
            {
                "name": "JHU_Bioinformatics_Portfolio",
                "path": "/Users/ugochi141/JHU_Bioinformatics_Portfolio",
                "type": "academic",
                "language": "python"
            }
        ]
        
        self.analysis_results = {
            "timestamp": datetime.now().isoformat(),
            "repositories": [],
            "summary": {},
            "recommendations": []
        }
        
    def analyze_repository(self, repo):
        """Analyze a single repository"""
        logger.info(f"Analyzing {repo['name']}...")
        
        repo_analysis = {
            "name": repo["name"],
            "path": repo["path"],
            "type": repo["type"],
            "language": repo["language"],
            "metrics": {},
            "issues": [],
            "status": "unknown"
        }
        
        if not os.path.exists(repo["path"]):
            repo_analysis["status"] = "not_found"
            return repo_analysis
            
        # Count files
        try:
            if repo["language"] == "python":
                py_files = list(Path(repo["path"]).rglob("*.py"))
                repo_analysis["metrics"]["python_files"] = len(py_files)
                repo_analysis["metrics"]["total_lines"] = sum(
                    len(open(f, 'r', errors='ignore').readlines()) 
                    for f in py_files if f.is_file()
                )
            elif repo["language"] == "javascript":
                js_files = list(Path(repo["path"]).rglob("*.js")) + list(Path(repo["path"]).rglob("*.jsx"))
                repo_analysis["metrics"]["javascript_files"] = len(js_files)
                
            # Check for tests
            test_dirs = ["tests", "test", "__tests__", "spec"]
            has_tests = any(
                (Path(repo["path"]) / test_dir).exists() 
                for test_dir in test_dirs
            )
            repo_analysis["metrics"]["has_tests"] = has_tests
            
            # Check for documentation
            doc_files = ["README.md", "README.rst", "README.txt", "docs"]
            has_docs = any(
                (Path(repo["path"]) / doc).exists() 
                for doc in doc_files
            )
            repo_analysis["metrics"]["has_documentation"] = has_docs
            
            # Check git status
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=repo["path"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                modified_files = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
                repo_analysis["metrics"]["uncommitted_changes"] = modified_files
                
                if modified_files > 10:
                    repo_analysis["issues"].append(f"{modified_files} uncommitted changes")
                    
            # Check last commit
            result = subprocess.run(
                ["git", "log", "-1", "--format=%cr"],
                cwd=repo["path"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                last_commit = result.stdout.strip()
                repo_analysis["metrics"]["last_commit"] = last_commit
                
            # Determine status
            if not has_tests:
                repo_analysis["issues"].append("No tests found")
            if not has_docs:
                repo_analysis["issues"].append("Missing documentation")
                
            if repo_analysis["issues"]:
                repo_analysis["status"] = "needs_attention"
            else:
                repo_analysis["status"] = "healthy"
                
        except Exception as e:
            logger.error(f"Error analyzing {repo['name']}: {e}")
            repo_analysis["status"] = "error"
            repo_analysis["issues"].append(str(e))
            
        return repo_analysis
        
    def generate_summary(self):
        """Generate analysis summary"""
        total_repos = len(self.analysis_results["repositories"])
        healthy = sum(1 for r in self.analysis_results["repositories"] if r["status"] == "healthy")
        needs_attention = sum(1 for r in self.analysis_results["repositories"] if r["status"] == "needs_attention")
        
        self.analysis_results["summary"] = {
            "total_repositories": total_repos,
            "healthy": healthy,
            "needs_attention": needs_attention,
            "with_tests": sum(1 for r in self.analysis_results["repositories"] 
                            if r["metrics"].get("has_tests", False)),
            "with_documentation": sum(1 for r in self.analysis_results["repositories"] 
                                    if r["metrics"].get("has_documentation", False)),
            "total_uncommitted_changes": sum(r["metrics"].get("uncommitted_changes", 0) 
                                           for r in self.analysis_results["repositories"])
        }
        
    def generate_recommendations(self):
        """Generate improvement recommendations"""
        for repo in self.analysis_results["repositories"]:
            if repo["status"] == "needs_attention":
                for issue in repo["issues"]:
                    if "tests" in issue.lower():
                        self.analysis_results["recommendations"].append({
                            "repository": repo["name"],
                            "priority": "high",
                            "action": "Add unit tests",
                            "benefit": "Improve code reliability and maintainability"
                        })
                    elif "documentation" in issue.lower():
                        self.analysis_results["recommendations"].append({
                            "repository": repo["name"],
                            "priority": "medium",
                            "action": "Add or update documentation",
                            "benefit": "Improve project accessibility and onboarding"
                        })
                    elif "uncommitted" in issue.lower():
                        self.analysis_results["recommendations"].append({
                            "repository": repo["name"],
                            "priority": "high",
                            "action": "Commit or stash changes",
                            "benefit": "Maintain clean repository state"
                        })
                        
    def save_analysis(self):
        """Save analysis results"""
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        
        report_file = reports_dir / "repo_analysis.json"
        with open(report_file, 'w') as f:
            json.dump(self.analysis_results, f, indent=2)
            
        logger.info(f"Analysis saved to {report_file}")
        
    def print_summary(self):
        """Print analysis summary"""
        print("\n" + "="*60)
        print("📊 REPOSITORY ANALYSIS SUMMARY")
        print("="*60)
        
        summary = self.analysis_results["summary"]
        print(f"\nTotal Repositories: {summary['total_repositories']}")
        print(f"✅ Healthy: {summary['healthy']}")
        print(f"⚠️  Needs Attention: {summary['needs_attention']}")
        print(f"🧪 With Tests: {summary['with_tests']}")
        print(f"📚 With Documentation: {summary['with_documentation']}")
        
        if summary['total_uncommitted_changes'] > 0:
            print(f"⚡ Total Uncommitted Changes: {summary['total_uncommitted_changes']}")
            
        if self.analysis_results["recommendations"]:
            print("\n💡 Top Recommendations:")
            for rec in self.analysis_results["recommendations"][:5]:
                print(f"  • [{rec['repository']}] {rec['action']}")
                
    def run(self):
        """Run complete analysis"""
        logger.info("Starting repository analysis...")
        
        for repo in self.repos:
            repo_analysis = self.analyze_repository(repo)
            self.analysis_results["repositories"].append(repo_analysis)
            
        self.generate_summary()
        self.generate_recommendations()
        self.save_analysis()
        self.print_summary()
        
        return 0 if self.analysis_results["summary"]["needs_attention"] == 0 else 1

def main():
    """Main function"""
    analyzer = RepositoryAnalyzer()
    return analyzer.run()

if __name__ == "__main__":
    exit(main())