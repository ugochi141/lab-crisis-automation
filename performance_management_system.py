#!/usr/bin/env python3
"""
Performance Management System
Kaiser Permanente Lab Automation System - Largo, MD

Addresses critical performance issues:
- TAT targets only 10-50% met (goal: 90%)
- Understaffed by 3.3 FTE
- Behavioral issues (sneaking off, long breaks)
- Poor QC and maintenance performance

Author: Lab Operations Manager
Date: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('performance_management.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PerformanceManagementSystem:
    """
    Comprehensive system to address performance and behavioral issues
    """
    
    def __init__(self):
        """
        Initialize the performance management system
        """
        self.critical_issues = {
            'tat_performance': {
                'current': 0.35,  # 35% target achievement
                'target': 0.90,  # 90% goal
                'gap': 0.55,     # 55% gap
                'priority': 'CRITICAL'
            },
            'staffing_gap': {
                'demand': 32.05,  # FTE needed
                'supply': 28.75,  # FTE available
                'gap': 3.3,       # 3.3 FTE short
                'priority': 'CRITICAL'
            },
            'peak_volume': {
                'peak_hours': '10am-3pm',
                'volume': 1700,   # patients
                'capacity': 1200,  # capacity
                'overflow': 500,   # overflow
                'priority': 'HIGH'
            },
            'behavioral_issues': {
                'sneaking_off': True,
                'long_breaks': True,
                'mistakes_hidden': True,
                'slow_qc': True,
                'priority': 'HIGH'
            }
        }
        
        self.staff_performance = {}
        self.action_plans = {}
        
        logger.info("Performance Management System initialized")
    
    def analyze_critical_performance_gaps(self) -> Dict:
        """
        Analyze the critical performance gaps identified
        """
        logger.info("Analyzing critical performance gaps...")
        
        analysis = {
            'tat_crisis': self._analyze_tat_crisis(),
            'staffing_crisis': self._analyze_staffing_crisis(),
            'volume_crisis': self._analyze_volume_crisis(),
            'behavioral_crisis': self._analyze_behavioral_crisis()
        }
        
        return analysis
    
    def _analyze_tat_crisis(self) -> Dict:
        """
        Analyze the TAT performance crisis
        """
        tat_analysis = {
            'current_state': {
                'overall_compliance': 0.35,  # 35%
                'stat_compliance': 0.25,    # 25%
                'routine_compliance': 0.40, # 40%
                'critical_compliance': 0.15 # 15%
            },
            'target_gaps': {
                'overall_gap': 0.55,  # 55% gap to 90% target
                'stat_gap': 0.65,     # 65% gap
                'routine_gap': 0.50,  # 50% gap
                'critical_gap': 0.75  # 75% gap
            },
            'root_causes': [
                'Insufficient staffing during peak hours',
                'Poor workflow efficiency',
                'Equipment downtime and maintenance issues',
                'Staff training gaps',
                'Inadequate quality control processes'
            ],
            'impact': {
                'patient_safety': 'HIGH RISK',
                'regulatory_compliance': 'FAILING',
                'operational_efficiency': 'POOR',
                'staff_morale': 'LOW'
            }
        }
        
        return tat_analysis
    
    def _analyze_staffing_crisis(self) -> Dict:
        """
        Analyze the staffing crisis
        """
        staffing_analysis = {
            'current_state': {
                'fte_demand': 32.05,
                'fte_supply': 28.75,
                'fte_gap': 3.3,
                'coverage_ratio': 0.90  # 90% coverage
            },
            'shift_analysis': {
                'day_shift': {
                    'demand': 12.0,
                    'supply': 10.5,
                    'gap': 1.5,
                    'coverage': 0.875
                },
                'evening_shift': {
                    'demand': 10.0,
                    'supply': 9.0,
                    'gap': 1.0,
                    'coverage': 0.90
                },
                'night_shift': {
                    'demand': 10.05,
                    'supply': 9.25,
                    'gap': 0.8,
                    'coverage': 0.92
                }
            },
            'impact': {
                'overtime_costs': 'HIGH',
                'burnout_risk': 'CRITICAL',
                'quality_risk': 'HIGH',
                'safety_risk': 'HIGH'
            }
        }
        
        return staffing_analysis
    
    def _analyze_volume_crisis(self) -> Dict:
        """
        Analyze the volume crisis during peak hours
        """
        volume_analysis = {
            'peak_hours': {
                'time_range': '10:00-15:00',
                'total_volume': 1700,
                'capacity': 1200,
                'overflow': 500,
                'overflow_percentage': 0.42  # 42% overflow
            },
            'hourly_breakdown': {
                '10:00': {'volume': 280, 'capacity': 200, 'overflow': 80},
                '11:00': {'volume': 320, 'capacity': 200, 'overflow': 120},
                '12:00': {'volume': 350, 'capacity': 200, 'overflow': 150},
                '13:00': {'volume': 320, 'capacity': 200, 'overflow': 120},
                '14:00': {'volume': 280, 'capacity': 200, 'overflow': 80},
                '15:00': {'volume': 150, 'capacity': 200, 'overflow': 0}
            },
            'impact': {
                'wait_times': 'EXCESSIVE',
                'patient_satisfaction': 'POOR',
                'staff_stress': 'CRITICAL',
                'quality_risk': 'HIGH'
            }
        }
        
        return volume_analysis
    
    def _analyze_behavioral_crisis(self) -> Dict:
        """
        Analyze the behavioral issues with direct reports
        """
        behavioral_analysis = {
            'identified_issues': {
                'sneaking_off': {
                    'frequency': 'DAILY',
                    'duration': '15-30 minutes',
                    'impact': 'HIGH',
                    'detection': 'DIFFICULT'
                },
                'long_breaks': {
                    'frequency': 'MULTIPLE_TIMES_PER_DAY',
                    'duration': '30-60 minutes',
                    'impact': 'HIGH',
                    'detection': 'MODERATE'
                },
                'hiding_mistakes': {
                    'frequency': 'REGULAR',
                    'types': ['QC errors', 'TAT delays', 'Documentation gaps'],
                    'impact': 'CRITICAL',
                    'detection': 'DIFFICULT'
                },
                'slow_performance': {
                    'qc_speed': '50%_below_target',
                    'maintenance_speed': '60%_below_target',
                    'general_work_speed': '40%_below_target',
                    'impact': 'HIGH'
                }
            },
            'root_causes': [
                'Lack of accountability',
                'Insufficient supervision',
                'Poor performance standards',
                'Inadequate training',
                'Low morale and engagement',
                'Inconsistent consequences'
            ],
            'impact': {
                'operational_efficiency': 'CRITICAL',
                'patient_safety': 'HIGH_RISK',
                'regulatory_compliance': 'FAILING',
                'team_morale': 'POOR',
                'management_credibility': 'LOW'
            }
        }
        
        return behavioral_analysis
    
    def create_immediate_action_plan(self) -> Dict:
        """
        Create immediate action plan to address critical issues
        """
        logger.info("Creating immediate action plan...")
        
        action_plan = {
            'immediate_actions': {
                'week_1': self._week_1_actions(),
                'week_2': self._week_2_actions(),
                'week_3': self._week_3_actions(),
                'week_4': self._week_4_actions()
            },
            'staffing_solutions': self._staffing_solutions(),
            'performance_monitoring': self._performance_monitoring_setup(),
            'behavioral_interventions': self._behavioral_interventions()
        }
        
        return action_plan
    
    def _week_1_actions(self) -> List[Dict]:
        """
        Week 1 immediate actions
        """
        return [
            {
                'action': 'Emergency Staff Meeting',
                'description': 'Address performance crisis and behavioral issues',
                'participants': 'All direct reports',
                'duration': '2 hours',
                'outcomes': ['Set clear expectations', 'Establish consequences', 'Create action plans']
            },
            {
                'action': 'Implement Real-time Monitoring',
                'description': 'Deploy tracking systems for TAT, breaks, and performance',
                'participants': 'IT, Management',
                'duration': '3 days',
                'outcomes': ['Live dashboard', 'Automated alerts', 'Performance tracking']
            },
            {
                'action': 'Staff Reallocation',
                'description': 'Move staff to cover peak hours and critical gaps',
                'participants': 'Management, HR',
                'duration': '1 day',
                'outcomes': ['Cover peak hours', 'Reduce TAT delays', 'Improve coverage']
            },
            {
                'action': 'QC Process Review',
                'description': 'Audit and improve quality control procedures',
                'participants': 'QC Team, Management',
                'duration': '2 days',
                'outcomes': ['Standardized procedures', 'Training plan', 'Monitoring system']
            }
        ]
    
    def _week_2_actions(self) -> List[Dict]:
        """
        Week 2 actions
        """
        return [
            {
                'action': 'Individual Performance Reviews',
                'description': 'One-on-one meetings with each direct report',
                'participants': 'Manager, Individual Staff',
                'duration': '1 hour each',
                'outcomes': ['Performance plans', 'Clear expectations', 'Consequences defined']
            },
            {
                'action': 'Cross-training Program',
                'description': 'Train staff for flexible deployment',
                'participants': 'All Staff',
                'duration': '3 days',
                'outcomes': ['Flexible staffing', 'Reduced idle time', 'Improved coverage']
            },
            {
                'action': 'Equipment Maintenance Schedule',
                'description': 'Implement preventive maintenance program',
                'participants': 'Maintenance Team',
                'duration': '2 days',
                'outcomes': ['Reduced downtime', 'Better reliability', 'Improved TAT']
            },
            {
                'action': 'Performance Incentives',
                'description': 'Implement reward system for good performance',
                'participants': 'HR, Management',
                'duration': '1 day',
                'outcomes': ['Motivation system', 'Clear rewards', 'Performance improvement']
            }
        ]
    
    def _week_3_actions(self) -> List[Dict]:
        """
        Week 3 actions
        """
        return [
            {
                'action': 'Process Optimization',
                'description': 'Streamline workflows for better efficiency',
                'participants': 'Process Team',
                'duration': '3 days',
                'outcomes': ['Improved efficiency', 'Reduced TAT', 'Better quality']
            },
            {
                'action': 'Advanced Training',
                'description': 'Provide advanced skills training',
                'participants': 'Training Team',
                'duration': '2 days',
                'outcomes': ['Skill improvement', 'Better performance', 'Reduced errors']
            },
            {
                'action': 'Team Building',
                'description': 'Improve team dynamics and communication',
                'participants': 'All Staff',
                'duration': '1 day',
                'outcomes': ['Better teamwork', 'Improved morale', 'Reduced conflicts']
            }
        ]
    
    def _week_4_actions(self) -> List[Dict]:
        """
        Week 4 actions
        """
        return [
            {
                'action': 'Performance Assessment',
                'description': 'Evaluate progress and adjust strategies',
                'participants': 'Management',
                'duration': '2 days',
                'outcomes': ['Progress report', 'Strategy adjustment', 'Next steps']
            },
            {
                'action': 'Long-term Planning',
                'description': 'Develop sustainable improvement plan',
                'participants': 'Management, HR',
                'duration': '2 days',
                'outcomes': ['Sustainable plan', 'Resource allocation', 'Success metrics']
            }
        ]
    
    def _staffing_solutions(self) -> Dict:
        """
        Immediate staffing solutions
        """
        return {
            'immediate_solutions': [
                {
                    'solution': 'Overtime Authorization',
                    'description': 'Authorize overtime for existing staff',
                    'fte_impact': '+2.0 FTE equivalent',
                    'cost': 'High',
                    'timeline': 'Immediate'
                },
                {
                    'solution': 'Temporary Staff',
                    'description': 'Hire temporary phlebotomists',
                    'fte_impact': '+3.3 FTE',
                    'cost': 'Medium',
                    'timeline': '1-2 weeks'
                },
                {
                    'solution': 'Cross-training',
                    'description': 'Train existing staff for multiple roles',
                    'fte_impact': '+1.5 FTE equivalent',
                    'cost': 'Low',
                    'timeline': '2-3 weeks'
                }
            ],
            'long_term_solutions': [
                {
                    'solution': 'Permanent Hiring',
                    'description': 'Hire 3-4 permanent phlebotomists',
                    'fte_impact': '+3.5 FTE',
                    'cost': 'Medium',
                    'timeline': '4-6 weeks'
                },
                {
                    'solution': 'Automation Implementation',
                    'description': 'Deploy automated systems',
                    'fte_impact': '+2.0 FTE equivalent',
                    'cost': 'High',
                    'timeline': '3-6 months'
                }
            ]
        }
    
    def _performance_monitoring_setup(self) -> Dict:
        """
        Set up comprehensive performance monitoring
        """
        return {
            'real_time_dashboards': [
                {
                    'dashboard': 'TAT Performance',
                    'metrics': ['STAT TAT', 'Routine TAT', 'Critical TAT'],
                    'alerts': ['TAT > 60 min', 'TAT > 90 min', 'TAT > 120 min'],
                    'update_frequency': 'Every 15 minutes'
                },
                {
                    'dashboard': 'Staff Activity',
                    'metrics': ['Break times', 'Idle time', 'Productivity'],
                    'alerts': ['Break > 30 min', 'Idle > 20 min', 'Low productivity'],
                    'update_frequency': 'Real-time'
                },
                {
                    'dashboard': 'Volume Management',
                    'metrics': ['Patient volume', 'Queue length', 'Wait times'],
                    'alerts': ['Volume > 120%', 'Queue > 20', 'Wait > 30 min'],
                    'update_frequency': 'Every 5 minutes'
                }
            ],
            'automated_alerts': [
                {
                    'alert_type': 'TAT Alert',
                    'condition': 'TAT > target by 20%',
                    'action': 'Notify supervisor immediately',
                    'escalation': 'Manager notification after 30 minutes'
                },
                {
                    'alert_type': 'Staff Alert',
                    'condition': 'Staff member away > 30 minutes',
                    'action': 'Notify supervisor',
                    'escalation': 'Manager notification after 1 hour'
                },
                {
                    'alert_type': 'Volume Alert',
                    'condition': 'Volume > 120% capacity',
                    'action': 'Activate backup staff',
                    'escalation': 'Emergency staffing after 1 hour'
                }
            ]
        }
    
    def _behavioral_interventions(self) -> Dict:
        """
        Behavioral intervention strategies
        """
        return {
            'immediate_interventions': [
                {
                    'intervention': 'Clear Expectations',
                    'description': 'Set specific, measurable performance standards',
                    'implementation': 'Document and communicate to all staff',
                    'timeline': 'Immediate'
                },
                {
                    'intervention': 'Consequence Management',
                    'description': 'Establish clear consequences for poor performance',
                    'implementation': 'Progressive discipline policy',
                    'timeline': 'Immediate'
                },
                {
                    'intervention': 'Increased Supervision',
                    'description': 'Implement more frequent check-ins and monitoring',
                    'implementation': 'Daily supervisor rounds',
                    'timeline': 'Immediate'
                }
            ],
            'support_interventions': [
                {
                    'intervention': 'Performance Coaching',
                    'description': 'Provide individual coaching for improvement',
                    'implementation': 'Weekly one-on-one sessions',
                    'timeline': 'Ongoing'
                },
                {
                    'intervention': 'Training Programs',
                    'description': 'Address skill gaps and improve performance',
                    'implementation': 'Targeted training sessions',
                    'timeline': '2-4 weeks'
                },
                {
                    'intervention': 'Recognition Programs',
                    'description': 'Reward good performance and behavior',
                    'implementation': 'Monthly recognition program',
                    'timeline': 'Ongoing'
                }
            ]
        }
    
    def generate_crisis_report(self) -> str:
        """
        Generate comprehensive crisis report
        """
        logger.info("Generating crisis report...")
        
        analysis = self.analyze_critical_performance_gaps()
        action_plan = self.create_immediate_action_plan()
        
        report = []
        report.append("=" * 80)
        report.append("CRITICAL PERFORMANCE CRISIS REPORT")
        report.append("Kaiser Permanente Lab Automation System - Largo, MD")
        report.append("=" * 80)
        report.append("")
        
        # Executive Summary
        report.append("EXECUTIVE SUMMARY")
        report.append("-" * 40)
        report.append("🚨 CRITICAL PERFORMANCE CRISIS IDENTIFIED")
        report.append("")
        report.append("Key Issues:")
        report.append("• TAT targets met only 35% (Goal: 90%)")
        report.append("• Understaffed by 3.3 FTE")
        report.append("• Peak volume overflow: 42%")
        report.append("• Behavioral issues: Sneaking off, long breaks, hiding mistakes")
        report.append("")
        
        # TAT Crisis
        report.append("TAT PERFORMANCE CRISIS")
        report.append("-" * 40)
        tat_data = analysis['tat_crisis']
        report.append(f"Current Compliance: {tat_data['current_state']['overall_compliance']:.1%}")
        report.append(f"Target Compliance: 90%")
        report.append(f"Performance Gap: {tat_data['target_gaps']['overall_gap']:.1%}")
        report.append("")
        report.append("Root Causes:")
        for cause in tat_data['root_causes']:
            report.append(f"• {cause}")
        report.append("")
        
        # Staffing Crisis
        report.append("STAFFING CRISIS")
        report.append("-" * 40)
        staffing_data = analysis['staffing_crisis']
        report.append(f"FTE Demand: {staffing_data['current_state']['fte_demand']}")
        report.append(f"FTE Supply: {staffing_data['current_state']['fte_supply']}")
        report.append(f"FTE Gap: {staffing_data['current_state']['fte_gap']}")
        report.append(f"Coverage Ratio: {staffing_data['current_state']['coverage_ratio']:.1%}")
        report.append("")
        
        # Volume Crisis
        report.append("VOLUME CRISIS")
        report.append("-" * 40)
        volume_data = analysis['volume_crisis']
        report.append(f"Peak Hours: {volume_data['peak_hours']['time_range']}")
        report.append(f"Total Volume: {volume_data['peak_hours']['total_volume']:,}")
        report.append(f"Capacity: {volume_data['peak_hours']['capacity']:,}")
        report.append(f"Overflow: {volume_data['peak_hours']['overflow']:,} ({volume_data['peak_hours']['overflow_percentage']:.1%})")
        report.append("")
        
        # Behavioral Crisis
        report.append("BEHAVIORAL CRISIS")
        report.append("-" * 40)
        behavioral_data = analysis['behavioral_crisis']
        report.append("Identified Issues:")
        for issue, details in behavioral_data['identified_issues'].items():
            if isinstance(details, dict):
                report.append(f"• {issue.replace('_', ' ').title()}: {details.get('frequency', 'Unknown')}")
        report.append("")
        
        # Immediate Action Plan
        report.append("IMMEDIATE ACTION PLAN")
        report.append("-" * 40)
        report.append("Week 1 - Emergency Response:")
        for action in action_plan['immediate_actions']['week_1']:
            report.append(f"• {action['action']}: {action['description']}")
        report.append("")
        
        # Staffing Solutions
        report.append("STAFFING SOLUTIONS")
        report.append("-" * 40)
        for solution in action_plan['staffing_solutions']['immediate_solutions']:
            report.append(f"• {solution['solution']}: {solution['description']} (+{solution['fte_impact']} FTE)")
        report.append("")
        
        # Behavioral Interventions
        report.append("BEHAVIORAL INTERVENTIONS")
        report.append("-" * 40)
        for intervention in action_plan['behavioral_interventions']['immediate_interventions']:
            report.append(f"• {intervention['intervention']}: {intervention['description']}")
        report.append("")
        
        # Success Metrics
        report.append("SUCCESS METRICS")
        report.append("-" * 40)
        report.append("30-Day Targets:")
        report.append("• TAT compliance: 35% → 60%")
        report.append("• Staff utilization: 67% → 80%")
        report.append("• Behavioral incidents: Reduce by 50%")
        report.append("• Peak volume overflow: 42% → 20%")
        report.append("")
        
        report.append("90-Day Targets:")
        report.append("• TAT compliance: 35% → 80%")
        report.append("• Staff utilization: 67% → 85%")
        report.append("• Behavioral incidents: Reduce by 80%")
        report.append("• Peak volume overflow: 42% → 10%")
        report.append("")
        
        report.append("=" * 80)
        report.append("Report generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        report.append("=" * 80)
        
        report_text = "\n".join(report)
        
        # Save report
        with open('critical_performance_crisis_report.txt', 'w') as f:
            f.write(report_text)
        
        logger.info("Critical performance crisis report generated")
        
        return report_text
    
    def create_management_dashboard(self) -> None:
        """
        Create management dashboard for oversight
        """
        logger.info("Creating management dashboard...")
        
        # Create dashboard visualization
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Performance Management Dashboard', fontsize=16, fontweight='bold')
        
        # TAT Performance
        tat_compliance = [0.35, 0.25, 0.40, 0.15]
        tat_labels = ['Overall', 'STAT', 'Routine', 'Critical']
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        
        axes[0, 0].bar(tat_labels, tat_compliance, color=colors)
        axes[0, 0].axhline(y=0.90, color='red', linestyle='--', label='Target (90%)')
        axes[0, 0].set_title('TAT Compliance Rates')
        axes[0, 0].set_ylabel('Compliance Rate')
        axes[0, 0].set_ylim(0, 1)
        axes[0, 0].legend()
        
        # Staffing Gap
        shifts = ['Day', 'Evening', 'Night']
        coverage = [0.875, 0.90, 0.92]
        
        axes[0, 1].bar(shifts, coverage, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        axes[0, 1].axhline(y=1.0, color='red', linestyle='--', label='Full Coverage')
        axes[0, 1].set_title('Staff Coverage by Shift')
        axes[0, 1].set_ylabel('Coverage Ratio')
        axes[0, 1].legend()
        
        # Peak Volume
        hours = ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00']
        volumes = [280, 320, 350, 320, 280, 150]
        capacity = [200, 200, 200, 200, 200, 200]
        
        axes[1, 0].bar(hours, capacity, color='lightblue', alpha=0.7, label='Capacity')
        axes[1, 0].bar(hours, volumes, color='red', alpha=0.7, label='Volume')
        axes[1, 0].set_title('Peak Hour Volume vs Capacity')
        axes[1, 0].set_ylabel('Patient Volume')
        axes[1, 0].legend()
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Behavioral Issues
        issues = ['Sneaking Off', 'Long Breaks', 'Hidden Mistakes', 'Slow QC']
        severity = [0.8, 0.7, 0.9, 0.6]
        
        axes[1, 1].bar(issues, severity, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
        axes[1, 1].set_title('Behavioral Issue Severity')
        axes[1, 1].set_ylabel('Severity Level')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('performance_management_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        logger.info("Management dashboard created and saved")


def main():
    """
    Main function to run the performance management system
    """
    print("Performance Management System")
    print("Kaiser Permanente Lab Automation System - Largo, MD")
    print("=" * 60)
    
    # Initialize system
    pms = PerformanceManagementSystem()
    
    # Generate crisis report
    try:
        report = pms.generate_crisis_report()
        print("\n" + "=" * 60)
        print("CRITICAL PERFORMANCE CRISIS REPORT")
        print("=" * 60)
        print(report)
        
        # Create dashboard
        pms.create_management_dashboard()
        
        print("\n" + "=" * 60)
        print("FILES GENERATED:")
        print("  - critical_performance_crisis_report.txt")
        print("  - performance_management_dashboard.png")
        print("  - performance_management.log")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error in performance management system: {str(e)}")
        logger.error(f"System error: {str(e)}")


if __name__ == "__main__":
    main()




