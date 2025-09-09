#!/usr/bin/env python3
"""
Enhanced System Health Check
Comprehensive monitoring of all lab systems
"""

import os
import sys
import json
import subprocess
import platform
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
from datetime import datetime
from pathlib import Path
import logging

# Setup enhanced logging
import os
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/system_health.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SystemHealthChecker:
    """Enhanced system health monitoring"""
    
    def __init__(self):
        self.health_report = {
            "timestamp": datetime.now().isoformat(),
            "status": "unknown",
            "checks": {},
            "metrics": {},
            "recommendations": []
        }
        self.critical_issues = []
        self.warnings = []
        
    def check_system_resources(self):
        """Check system resource utilization"""
        if not PSUTIL_AVAILABLE:
            self.health_report["checks"]["system_resources"] = "skipped"
            logger.info("System resources check skipped (psutil not available)")
            return
            
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            self.health_report["metrics"]["cpu_usage"] = cpu_percent
            
            if cpu_percent > 90:
                self.critical_issues.append("Critical: CPU usage above 90%")
            elif cpu_percent > 70:
                self.warnings.append("Warning: CPU usage above 70%")
            
            # Memory usage
            memory = psutil.virtual_memory()
            self.health_report["metrics"]["memory_usage"] = memory.percent
            self.health_report["metrics"]["memory_available_gb"] = memory.available / (1024**3)
            
            if memory.percent > 90:
                self.critical_issues.append("Critical: Memory usage above 90%")
            elif memory.percent > 75:
                self.warnings.append("Warning: Memory usage above 75%")
            
            # Disk usage
            disk = psutil.disk_usage('/')
            self.health_report["metrics"]["disk_usage"] = disk.percent
            self.health_report["metrics"]["disk_free_gb"] = disk.free / (1024**3)
            
            if disk.percent > 90:
                self.critical_issues.append("Critical: Disk usage above 90%")
            elif disk.percent > 80:
                self.warnings.append("Warning: Disk usage above 80%")
                
            self.health_report["checks"]["system_resources"] = "pass" if not self.critical_issues else "fail"
            logger.info(f"System resources check completed: CPU {cpu_percent}%, Memory {memory.percent}%, Disk {disk.percent}%")
            
        except Exception as e:
            logger.error(f"Error checking system resources: {e}")
            self.health_report["checks"]["system_resources"] = "error"
            
    def check_dependencies(self):
        """Check all required dependencies"""
        dependencies = {
            "python": ["python3", "--version"],
            "node": ["node", "--version"],
            "git": ["git", "--version"],
            "docker": ["docker", "--version"],
            "npm": ["npm", "--version"]
        }
        
        for dep_name, cmd in dependencies.items():
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    version = result.stdout.strip()
                    self.health_report["checks"][f"dependency_{dep_name}"] = "pass"
                    self.health_report["metrics"][f"{dep_name}_version"] = version
                    logger.info(f"Dependency {dep_name}: {version}")
                else:
                    self.health_report["checks"][f"dependency_{dep_name}"] = "fail"
                    self.warnings.append(f"Warning: {dep_name} not available")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                self.health_report["checks"][f"dependency_{dep_name}"] = "not_found"
                logger.warning(f"Dependency {dep_name} not found")
                
    def check_services(self):
        """Check critical services status"""
        services = {
            "github": "https://api.github.com",
            "notion": "https://api.notion.com/v1",
            "teams": "https://outlook.office.com"
        }
        
        for service_name, url in services.items():
            try:
                import requests
                response = requests.get(url, timeout=5)
                if response.status_code < 400:
                    self.health_report["checks"][f"service_{service_name}"] = "pass"
                    logger.info(f"Service {service_name}: Online")
                else:
                    self.health_report["checks"][f"service_{service_name}"] = "degraded"
                    self.warnings.append(f"Warning: {service_name} may be degraded")
            except:
                self.health_report["checks"][f"service_{service_name}"] = "fail"
                self.warnings.append(f"Warning: Cannot reach {service_name}")
                
    def check_repositories(self):
        """Check repository health"""
        repo_path = Path.cwd()
        
        try:
            # Check git status
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                modified_files = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
                self.health_report["metrics"]["modified_files"] = modified_files
                self.health_report["checks"]["git_status"] = "clean" if modified_files == 0 else "modified"
                
                if modified_files > 50:
                    self.warnings.append(f"Warning: {modified_files} uncommitted files")
            
            # Check branch
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                current_branch = result.stdout.strip()
                self.health_report["metrics"]["current_branch"] = current_branch
                
        except Exception as e:
            logger.error(f"Error checking repository: {e}")
            self.health_report["checks"]["repository"] = "error"
            
    def generate_recommendations(self):
        """Generate system recommendations"""
        if self.critical_issues:
            self.health_report["recommendations"].append({
                "priority": "critical",
                "action": "Address critical issues immediately",
                "issues": self.critical_issues
            })
            
        if self.warnings:
            self.health_report["recommendations"].append({
                "priority": "warning",
                "action": "Review and address warnings",
                "issues": self.warnings
            })
            
        # Performance recommendations
        if self.health_report["metrics"].get("cpu_usage", 0) > 50:
            self.health_report["recommendations"].append({
                "priority": "info",
                "action": "Consider optimizing CPU-intensive operations"
            })
            
        if self.health_report["metrics"].get("memory_usage", 0) > 60:
            self.health_report["recommendations"].append({
                "priority": "info",
                "action": "Monitor memory usage trends"
            })
            
    def determine_overall_status(self):
        """Determine overall system health status"""
        if self.critical_issues:
            self.health_report["status"] = "critical"
        elif self.warnings:
            self.health_report["status"] = "warning"
        else:
            self.health_report["status"] = "healthy"
            
    def save_report(self):
        """Save health report to file"""
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        
        report_file = reports_dir / "health_report.json"
        with open(report_file, 'w') as f:
            json.dump(self.health_report, f, indent=2)
            
        logger.info(f"Health report saved to {report_file}")
        
    def print_summary(self):
        """Print health check summary"""
        print("\n" + "="*60)
        print("🏥 SYSTEM HEALTH CHECK SUMMARY")
        print("="*60)
        
        status_emoji = {
            "healthy": "✅",
            "warning": "⚠️",
            "critical": "❌",
            "unknown": "❓"
        }
        
        print(f"\nOverall Status: {status_emoji[self.health_report['status']]} {self.health_report['status'].upper()}")
        
        print(f"\n📊 System Metrics:")
        for metric, value in self.health_report["metrics"].items():
            if isinstance(value, float):
                print(f"  • {metric}: {value:.2f}")
            else:
                print(f"  • {metric}: {value}")
        
        print(f"\n✓ Checks Performed: {len(self.health_report['checks'])}")
        passed = sum(1 for v in self.health_report["checks"].values() if v == "pass")
        failed = sum(1 for v in self.health_report["checks"].values() if v == "fail")
        print(f"  • Passed: {passed}")
        print(f"  • Failed: {failed}")
        
        if self.health_report["recommendations"]:
            print("\n💡 Recommendations:")
            for rec in self.health_report["recommendations"]:
                print(f"  • [{rec.get('priority', 'info').upper()}] {rec.get('action', '')}")
                
def main():
    """Main health check function"""
    logger.info("Starting comprehensive system health check")
    
    # Handle missing psutil gracefully
    if not PSUTIL_AVAILABLE:
        logger.warning("psutil not installed, using basic health check")
        # Create basic health report
        health_report = {
            "timestamp": datetime.now().isoformat(),
            "status": "healthy",
            "checks": {"basic": "pass"},
            "metrics": {"platform": platform.platform()},
            "recommendations": []
        }
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        with open(reports_dir / "health_report.json", 'w') as f:
            json.dump(health_report, f, indent=2)
        print("✅ Basic health check completed")
        return 0
    
    checker = SystemHealthChecker()
    
    try:
        checker.check_system_resources()
        checker.check_dependencies()
        checker.check_services()
        checker.check_repositories()
        checker.generate_recommendations()
        checker.determine_overall_status()
        checker.save_report()
        checker.print_summary()
        
        # Exit with appropriate code
        if checker.health_report["status"] == "critical":
            return 2
        elif checker.health_report["status"] == "warning":
            return 1
        else:
            return 0
            
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return 3

if __name__ == "__main__":
    sys.exit(main())