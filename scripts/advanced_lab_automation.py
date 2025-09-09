#!/usr/bin/env python3
"""
Advanced Lab Automation System
Comprehensive enhancement with AI-powered features
"""

import os
import sys
import json
import time
import logging
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from notion_client import Client
from dotenv import load_dotenv
from typing import Dict, List, Optional, Tuple
import asyncio
import aiohttp
from dataclasses import dataclass
from enum import Enum

# Load environment variables
load_dotenv()

# Configure enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/advanced_lab_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AlertSeverity(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

@dataclass
class LabMetric:
    name: str
    value: float
    target: float
    unit: str
    timestamp: datetime
    severity: AlertSeverity

@dataclass
class StaffMember:
    id: str
    name: str
    role: str
    shift: str
    performance_score: float
    last_break: datetime
    current_task: str
    status: str

class AdvancedLabAutomation:
    """Advanced Lab Automation with AI-powered features"""
    
    def __init__(self):
        self.notion_token = os.getenv('NOTION_API_TOKEN')
        self.teams_webhook = os.getenv('TEAMS_WEBHOOK_URL')
        self.performance_db_id = os.getenv('NOTION_PERFORMANCE_DB_ID')
        self.incident_db_id = os.getenv('NOTION_INCIDENT_DB_ID')
        self.lab_management_center = os.getenv('NOTION_LAB_MANAGEMENT_CENTER')
        
        # Initialize clients
        self.notion = None
        self.session = None
        
        # Configuration
        self.alert_thresholds = {
            'tat_compliance': 90.0,
            'wait_time': 15.0,
            'staffing_gap': 0.0,
            'error_rate': 5.0,
            'staff_utilization': 80.0,
            'break_time': 15.0,
            'qc_completion': 95.0
        }
        
        # AI Models (simplified for demo)
        self.prediction_models = {
            'workload_prediction': self._predict_workload,
            'staff_optimization': self._optimize_staffing,
            'anomaly_detection': self._detect_anomalies,
            'performance_scoring': self._calculate_performance_score
        }
        
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize external service clients"""
        try:
            if self.notion_token and self.notion_token != 'your_notion_token_here':
                self.notion = Client(auth=self.notion_token)
                logger.info("✅ Notion client initialized")
            else:
                logger.warning("⚠️ Notion token not configured")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Notion client: {e}")
    
    async def _initialize_async_session(self):
        """Initialize async HTTP session"""
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def _close_async_session(self):
        """Close async HTTP session"""
        if self.session:
            await self.session.close()
    
    def _predict_workload(self, historical_data: List[Dict]) -> Dict:
        """AI-powered workload prediction"""
        # Simplified prediction algorithm
        if not historical_data:
            return {'predicted_volume': 100, 'confidence': 0.5}
        
        # Calculate trend
        volumes = [d.get('volume', 0) for d in historical_data[-7:]]  # Last 7 days
        if len(volumes) < 2:
            return {'predicted_volume': 100, 'confidence': 0.5}
        
        trend = np.polyfit(range(len(volumes)), volumes, 1)[0]
        predicted_volume = volumes[-1] + trend
        
        # Calculate confidence based on data consistency
        variance = np.var(volumes)
        confidence = max(0.1, min(0.9, 1 - (variance / 1000)))
        
        return {
            'predicted_volume': max(0, predicted_volume),
            'confidence': confidence,
            'trend': 'increasing' if trend > 0 else 'decreasing'
        }
    
    def _optimize_staffing(self, current_staff: List[StaffMember], predicted_workload: Dict) -> Dict:
        """AI-powered staffing optimization"""
        current_count = len(current_staff)
        predicted_volume = predicted_workload.get('predicted_volume', 100)
        
        # Simple optimization: 1 staff per 20 samples
        optimal_count = max(1, int(predicted_volume / 20))
        
        # Check for over/under staffing
        if current_count < optimal_count:
            gap = optimal_count - current_count
            return {
                'status': 'UNDERSTAFFED',
                'current_count': current_count,
                'optimal_count': optimal_count,
                'gap': gap,
                'recommendation': f'Add {gap} staff members'
            }
        elif current_count > optimal_count * 1.2:
            excess = current_count - optimal_count
            return {
                'status': 'OVERSTAFFED',
                'current_count': current_count,
                'optimal_count': optimal_count,
                'excess': excess,
                'recommendation': f'Consider reducing by {excess} staff members'
            }
        else:
            return {
                'status': 'OPTIMAL',
                'current_count': current_count,
                'optimal_count': optimal_count,
                'recommendation': 'Staffing levels are optimal'
            }
    
    def _detect_anomalies(self, metrics: List[LabMetric]) -> List[Dict]:
        """AI-powered anomaly detection"""
        anomalies = []
        
        for metric in metrics:
            # Simple anomaly detection based on standard deviation
            if metric.value > metric.target * 2:
                anomalies.append({
                    'metric': metric.name,
                    'value': metric.value,
                    'target': metric.target,
                    'severity': 'HIGH',
                    'description': f'{metric.name} is {metric.value/metric.target:.1f}x above target'
                })
            elif metric.value > metric.target * 1.5:
                anomalies.append({
                    'metric': metric.name,
                    'value': metric.value,
                    'target': metric.target,
                    'severity': 'MEDIUM',
                    'description': f'{metric.name} is {metric.value/metric.target:.1f}x above target'
                })
        
        return anomalies
    
    def _calculate_performance_score(self, staff_member: StaffMember, metrics: List[LabMetric]) -> float:
        """AI-powered performance scoring"""
        # Weighted performance calculation
        weights = {
            'tat_compliance': 0.3,
            'error_rate': 0.25,
            'utilization': 0.2,
            'break_efficiency': 0.15,
            'qc_completion': 0.1
        }
        
        score = 0.0
        for metric in metrics:
            if metric.name in weights:
                # Normalize metric value (0-100 scale)
                normalized_value = min(100, max(0, (metric.value / metric.target) * 100))
                score += normalized_value * weights[metric.name]
        
        return min(100, max(0, score))
    
    async def collect_real_time_metrics(self) -> List[LabMetric]:
        """Collect real-time lab metrics"""
        logger.info("🔍 Collecting real-time metrics...")
        
        # Simulate real-time data collection
        current_time = datetime.now()
        
        metrics = [
            LabMetric("TAT Compliance", 35.0, 90.0, "%", current_time, AlertSeverity.CRITICAL),
            LabMetric("Wait Time", 25.0, 15.0, "minutes", current_time, AlertSeverity.HIGH),
            LabMetric("Staffing Gap", 3.3, 0.0, "positions", current_time, AlertSeverity.HIGH),
            LabMetric("Error Rate", 12.0, 5.0, "%", current_time, AlertSeverity.CRITICAL),
            LabMetric("Staff Utilization", 67.6, 80.0, "%", current_time, AlertSeverity.MEDIUM),
            LabMetric("Break Time", 18.0, 15.0, "minutes", current_time, AlertSeverity.MEDIUM),
            LabMetric("QC Completion", 88.0, 95.0, "%", current_time, AlertSeverity.MEDIUM)
        ]
        
        return metrics
    
    async def analyze_staff_performance(self) -> List[StaffMember]:
        """Analyze staff performance with AI insights"""
        logger.info("👥 Analyzing staff performance...")
        
        # Simulate staff data
        staff = [
            StaffMember("001", "John Smith", "Senior Tech", "Day", 85.5, 
                       datetime.now() - timedelta(minutes=30), "Sample Processing", "Active"),
            StaffMember("002", "Jane Doe", "Lab Tech", "Day", 72.3, 
                       datetime.now() - timedelta(minutes=45), "QC Testing", "Active"),
            StaffMember("003", "Mike Johnson", "Lab Tech", "Evening", 68.9, 
                       datetime.now() - timedelta(minutes=60), "Sample Prep", "On Break"),
            StaffMember("004", "Sarah Wilson", "Senior Tech", "Night", 91.2, 
                       datetime.now() - timedelta(minutes=15), "Result Verification", "Active")
        ]
        
        return staff
    
    async def generate_ai_insights(self, metrics: List[LabMetric], staff: List[StaffMember]) -> Dict:
        """Generate AI-powered insights and recommendations"""
        logger.info("🤖 Generating AI insights...")
        
        # Workload prediction
        historical_data = [{'volume': 120, 'timestamp': datetime.now() - timedelta(days=i)} for i in range(7)]
        workload_prediction = self.prediction_models['workload_prediction'](historical_data)
        
        # Staffing optimization
        staffing_analysis = self.prediction_models['staff_optimization'](staff, workload_prediction)
        
        # Anomaly detection
        anomalies = self.prediction_models['anomaly_detection'](metrics)
        
        # Performance scoring for each staff member
        performance_scores = {}
        for member in staff:
            score = self.prediction_models['performance_scoring'](member, metrics)
            performance_scores[member.id] = {
                'name': member.name,
                'score': score,
                'grade': 'A' if score >= 90 else 'B' if score >= 80 else 'C' if score >= 70 else 'D'
            }
        
        insights = {
            'timestamp': datetime.now().isoformat(),
            'workload_prediction': workload_prediction,
            'staffing_analysis': staffing_analysis,
            'anomalies': anomalies,
            'performance_scores': performance_scores,
            'recommendations': self._generate_recommendations(metrics, staff, anomalies, staffing_analysis)
        }
        
        return insights
    
    def _generate_recommendations(self, metrics: List[LabMetric], staff: List[StaffMember], 
                                 anomalies: List[Dict], staffing_analysis: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # TAT Compliance recommendations
        tat_metric = next((m for m in metrics if m.name == "TAT Compliance"), None)
        if tat_metric and tat_metric.value < 60:
            recommendations.append("🚨 URGENT: Implement emergency TAT protocols - consider overtime or additional staff")
        
        # Staffing recommendations
        if staffing_analysis['status'] == 'UNDERSTAFFED':
            recommendations.append(f"👥 STAFFING: {staffing_analysis['recommendation']}")
        elif staffing_analysis['status'] == 'OVERSTAFFED':
            recommendations.append(f"👥 EFFICIENCY: {staffing_analysis['recommendation']}")
        
        # Error rate recommendations
        error_metric = next((m for m in metrics if m.name == "Error Rate"), None)
        if error_metric and error_metric.value > 10:
            recommendations.append("🔧 QUALITY: Implement additional QC checks and staff training")
        
        # Break time recommendations
        break_metric = next((m for m in metrics if m.name == "Break Time"), None)
        if break_metric and break_metric.value > 20:
            recommendations.append("⏰ EFFICIENCY: Review break scheduling to reduce wait times")
        
        return recommendations
    
    async def create_notion_entries(self, insights: Dict) -> bool:
        """Create enhanced Notion entries with AI insights"""
        if not self.notion:
            logger.error("❌ Notion not configured")
            return False
        
        try:
            # Create performance entry
            if self.performance_db_id:
                performance_data = {
                    "Timestamp": {"date": {"start": insights['timestamp']}},
                    "AI Insights": {"rich_text": [{"text": {"content": json.dumps(insights, indent=2)}}]},
                    "Workload Prediction": {"number": insights['workload_prediction']['predicted_volume']},
                    "Staffing Status": {"select": {"name": insights['staffing_analysis']['status']}},
                    "Anomalies Detected": {"number": len(insights['anomalies'])},
                    "Recommendations": {"rich_text": [{"text": {"content": "\\n".join(insights['recommendations'])}}]}
                }
                
                self.notion.pages.create(
                    parent={"database_id": self.performance_db_id},
                    properties=performance_data
                )
                logger.info("✅ Created performance entry in Notion")
            
            # Create incident entries for anomalies
            if self.incident_db_id and insights['anomalies']:
                for anomaly in insights['anomalies']:
                    incident_data = {
                        "Alert Type": {"title": [{"text": {"content": f"AI Detected Anomaly: {anomaly['metric']}"}}]},
                        "Message": {"rich_text": [{"text": {"content": anomaly['description']}}]},
                        "Severity": {"select": {"name": anomaly['severity']}},
                        "Timestamp": {"date": {"start": insights['timestamp']}},
                        "Status": {"select": {"name": "Active"}},
                        "AI Generated": {"checkbox": True}
                    }
                    
                    self.notion.pages.create(
                        parent={"database_id": self.incident_db_id},
                        properties=incident_data
                    )
                logger.info(f"✅ Created {len(insights['anomalies'])} incident entries")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create Notion entries: {e}")
            return False
    
    async def send_enhanced_teams_alert(self, insights: Dict) -> bool:
        """Send enhanced Teams alert with AI insights"""
        if not self.teams_webhook or self.teams_webhook == 'your_teams_webhook_url_here':
            logger.warning("⚠️ Teams webhook not configured")
            return False
        
        # Determine alert color based on severity
        critical_issues = len([a for a in insights['anomalies'] if a['severity'] == 'HIGH'])
        if critical_issues > 0:
            color = "FF0000"  # Red
            title = "🚨 CRITICAL Lab Issues Detected"
        elif insights['staffing_analysis']['status'] == 'UNDERSTAFFED':
            color = "FFA500"  # Orange
            title = "⚠️ Lab Staffing Alert"
        else:
            color = "00FF00"  # Green
            title = "✅ Lab Status Update"
        
        # Create enhanced message
        message_sections = [
            f"**🤖 AI-Powered Lab Analysis - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**",
            "",
            "**📊 Key Metrics:**",
            f"• Workload Prediction: {insights['workload_prediction']['predicted_volume']} samples (Confidence: {insights['workload_prediction']['confidence']:.1%})",
            f"• Staffing Status: {insights['staffing_analysis']['status']}",
            f"• Anomalies Detected: {len(insights['anomalies'])}",
            "",
            "**🎯 AI Recommendations:**"
        ]
        
        for i, rec in enumerate(insights['recommendations'][:5], 1):  # Limit to top 5
            message_sections.append(f"{i}. {rec}")
        
        if len(insights['recommendations']) > 5:
            message_sections.append(f"... and {len(insights['recommendations']) - 5} more recommendations")
        
        payload = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": color,
            "summary": title,
            "sections": [{
                "activityTitle": title,
                "activitySubtitle": "Advanced Lab Automation System",
                "activityImage": "https://img.icons8.com/color/48/000000/artificial-intelligence.png",
                "text": "\\n".join(message_sections),
                "markdown": True
            }]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.teams_webhook,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        logger.info("✅ Enhanced Teams alert sent successfully")
                        return True
                    else:
                        logger.error(f"❌ Teams webhook failed: {response.status}")
                        return False
        except Exception as e:
            logger.error(f"❌ Failed to send Teams alert: {e}")
            return False
    
    async def run_advanced_monitoring_cycle(self) -> bool:
        """Run complete advanced monitoring cycle"""
        logger.info("🚀 Starting advanced monitoring cycle...")
        
        try:
            # Initialize async session
            await self._initialize_async_session()
            
            # Collect data
            metrics = await self.collect_real_time_metrics()
            staff = await self.analyze_staff_performance()
            
            # Generate AI insights
            insights = await self.generate_ai_insights(metrics, staff)
            
            # Create Notion entries
            notion_success = await self.create_notion_entries(insights)
            
            # Send Teams alert
            teams_success = await self.send_enhanced_teams_alert(insights)
            
            # Log results
            logger.info(f"📊 Metrics collected: {len(metrics)}")
            logger.info(f"👥 Staff analyzed: {len(staff)}")
            logger.info(f"🤖 AI insights generated: {len(insights['recommendations'])} recommendations")
            logger.info(f"📝 Notion entries: {'✅' if notion_success else '❌'}")
            logger.info(f"📱 Teams alert: {'✅' if teams_success else '❌'}")
            
            return notion_success or teams_success
            
        except Exception as e:
            logger.error(f"❌ Advanced monitoring cycle failed: {e}")
            return False
        finally:
            await self._close_async_session()

async def main():
    """Main execution function"""
    print("🏥 Advanced Lab Automation System")
    print("=" * 50)
    print("🤖 AI-Powered Features:")
    print("• Workload Prediction")
    print("• Staffing Optimization")
    print("• Anomaly Detection")
    print("• Performance Scoring")
    print("• Intelligent Recommendations")
    print("=" * 50)
    
    # Create necessary directories
    os.makedirs('logs', exist_ok=True)
    
    # Initialize system
    automation = AdvancedLabAutomation()
    
    # Run monitoring cycle
    success = await automation.run_advanced_monitoring_cycle()
    
    if success:
        print("✅ Advanced monitoring cycle completed successfully")
    else:
        print("❌ Advanced monitoring cycle failed")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
