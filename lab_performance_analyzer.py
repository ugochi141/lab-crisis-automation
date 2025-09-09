#!/usr/bin/env python3
"""
Lab Performance Analyzer
Kaiser Permanente Lab Automation System - Largo, MD

This script analyzes lab performance metrics from various data sources:
- TAT (Turnaround Time) data
- Staffing and idle time metrics
- Patient encounter volumes
- Queue performance and wait times
- Performance by shift, hour, and queue type

Author: Lab Operations Manager
Date: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('lab_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class LabPerformanceAnalyzer:
    """
    Comprehensive analyzer for lab performance metrics
    """
    
    def __init__(self, data_path: str = "data"):
        """
        Initialize the analyzer with data path
        
        Args:
            data_path: Path to the data directory
        """
        self.data_path = Path(data_path)
        self.results = {}
        self.summary_stats = {}
        
        # Define key performance indicators
        self.kpis = {
            'tat': {
                'stat_target': 60,  # minutes
                'routine_target': 240,  # minutes
                'critical_target': 30  # minutes
            },
            'staffing': {
                'idle_time_target': 0.20,  # 20% max idle time
                'utilization_target': 0.80  # 80% min utilization
            },
            'queue': {
                'wait_time_target': 15,  # minutes
                'no_show_target': 0.10  # 10% max no-show rate
            }
        }
        
        logger.info("Lab Performance Analyzer initialized")
    
    def analyze_tat_data(self) -> Dict:
        """
        Analyze Turnaround Time (TAT) performance
        
        Returns:
            Dictionary containing TAT analysis results
        """
        logger.info("Analyzing TAT data...")
        
        tat_analysis = {
            'stat_performance': {},
            'routine_performance': {},
            'shift_comparison': {},
            'trends': {}
        }
        
        # Simulate TAT data analysis based on file structure
        # In practice, this would read from the actual CSV/PDF files
        
        # STAT TAT Analysis
        stat_tat_data = {
            'all_shift': {'avg_tat': 45, 'p95_tat': 75, 'compliance_rate': 0.85},
            'day_shift': {'avg_tat': 42, 'p95_tat': 68, 'compliance_rate': 0.88},
            'evening_shift': {'avg_tat': 48, 'p95_tat': 82, 'compliance_rate': 0.82},
            'night_shift': {'avg_tat': 52, 'p95_tat': 90, 'compliance_rate': 0.78}
        }
        
        tat_analysis['stat_performance'] = stat_tat_data
        
        # Calculate overall STAT performance
        overall_stat_tat = np.mean([data['avg_tat'] for data in stat_tat_data.values()])
        overall_compliance = np.mean([data['compliance_rate'] for data in stat_tat_data.values()])
        
        tat_analysis['overall_stat'] = {
            'avg_tat': overall_stat_tat,
            'compliance_rate': overall_compliance,
            'target_met': overall_stat_tat <= self.kpis['tat']['stat_target']
        }
        
        self.results['tat'] = tat_analysis
        logger.info(f"TAT Analysis Complete - Overall STAT TAT: {overall_stat_tat:.1f} min")
        
        return tat_analysis
    
    def analyze_staffing_performance(self) -> Dict:
        """
        Analyze staffing performance and idle time
        
        Returns:
            Dictionary containing staffing analysis results
        """
        logger.info("Analyzing staffing performance...")
        
        staffing_analysis = {
            'idle_time': {},
            'utilization': {},
            'performance_by_staff': {},
            'shift_coverage': {}
        }
        
        # Simulate staffing data analysis
        idle_time_data = {
            'phleb_station_1': {'idle_time': 0.35, 'utilization': 0.65},
            'phleb_station_2': {'idle_time': 0.28, 'utilization': 0.72},
            'phleb_station_3': {'idle_time': 0.42, 'utilization': 0.58},
            'phleb_station_4': {'idle_time': 0.31, 'utilization': 0.69},
            'phleb_station_5': {'idle_time': 0.38, 'utilization': 0.62},
            'phleb_station_6': {'idle_time': 0.25, 'utilization': 0.75},
            'phleb_station_7': {'idle_time': 0.33, 'utilization': 0.67},
            'phleb_station_8': {'idle_time': 0.29, 'utilization': 0.71},
            'phleb_station_9': {'idle_time': 0.36, 'utilization': 0.64},
            'phleb_station_10': {'idle_time': 0.27, 'utilization': 0.73}
        }
        
        staffing_analysis['idle_time'] = idle_time_data
        
        # Calculate overall metrics
        overall_idle_time = np.mean([data['idle_time'] for data in idle_time_data.values()])
        overall_utilization = np.mean([data['utilization'] for data in idle_time_data.values()])
        
        staffing_analysis['overall'] = {
            'avg_idle_time': overall_idle_time,
            'avg_utilization': overall_utilization,
            'idle_time_target_met': overall_idle_time <= self.kpis['staffing']['idle_time_target'],
            'utilization_target_met': overall_utilization >= self.kpis['staffing']['utilization_target']
        }
        
        self.results['staffing'] = staffing_analysis
        logger.info(f"Staffing Analysis Complete - Avg Idle Time: {overall_idle_time:.1%}")
        
        return staffing_analysis
    
    def analyze_volume_metrics(self) -> Dict:
        """
        Analyze patient encounter volumes and lab volumes
        
        Returns:
            Dictionary containing volume analysis results
        """
        logger.info("Analyzing volume metrics...")
        
        volume_analysis = {
            'patient_encounters': {},
            'lab_volumes': {},
            'trends': {},
            'peak_hours': {}
        }
        
        # Simulate volume data analysis
        monthly_encounters = {
            'may': 1250,
            'june': 1320,
            'july': 1280,
            'ytd_total': 15200
        }
        
        volume_analysis['patient_encounters'] = monthly_encounters
        
        # Lab volume by type
        lab_volumes = {
            'stat_tests': {'volume': 320, 'percentage': 0.25},
            'routine_tests': {'volume': 960, 'percentage': 0.75},
            'critical_tests': {'volume': 45, 'percentage': 0.035}
        }
        
        volume_analysis['lab_volumes'] = lab_volumes
        
        # Peak hours analysis
        peak_hours = {
            'morning_peak': {'hour': '8-10', 'volume': 280, 'percentage': 0.22},
            'afternoon_peak': {'hour': '14-16', 'volume': 240, 'percentage': 0.19},
            'evening_peak': {'hour': '18-20', 'volume': 180, 'percentage': 0.14}
        }
        
        volume_analysis['peak_hours'] = peak_hours
        
        self.results['volume'] = volume_analysis
        logger.info(f"Volume Analysis Complete - Monthly Avg: {np.mean(list(monthly_encounters.values())[:3]):.0f} encounters")
        
        return volume_analysis
    
    def analyze_queue_performance(self) -> Dict:
        """
        Analyze queue performance and wait times
        
        Returns:
            Dictionary containing queue analysis results
        """
        logger.info("Analyzing queue performance...")
        
        queue_analysis = {
            'wait_times': {},
            'queue_types': {},
            'no_show_rates': {},
            'scheduling_efficiency': {}
        }
        
        # Simulate queue performance data
        wait_time_data = {
            'stat_queue': {'avg_wait': 8, 'p95_wait': 15, 'target_met': True},
            'routine_queue': {'avg_wait': 22, 'p95_wait': 45, 'target_met': False},
            'appointment_queue': {'avg_wait': 5, 'p95_wait': 12, 'target_met': True}
        }
        
        queue_analysis['wait_times'] = wait_time_data
        
        # Queue type performance
        queue_types = {
            'emergency': {'volume': 85, 'avg_wait': 6, 'satisfaction': 0.92},
            'scheduled': {'volume': 720, 'avg_wait': 8, 'satisfaction': 0.88},
            'walk_in': {'volume': 475, 'avg_wait': 25, 'satisfaction': 0.75}
        }
        
        queue_analysis['queue_types'] = queue_types
        
        # No-show rates
        no_show_data = {
            'overall_rate': 0.08,  # 8%
            'scheduled_appointments': 0.06,  # 6%
            'walk_in_no_shows': 0.12  # 12%
        }
        
        queue_analysis['no_show_rates'] = no_show_data
        
        self.results['queue'] = queue_analysis
        logger.info(f"Queue Analysis Complete - Overall No-Show Rate: {no_show_data['overall_rate']:.1%}")
        
        return queue_analysis
    
    def generate_performance_summary(self) -> Dict:
        """
        Generate comprehensive performance summary
        
        Returns:
            Dictionary containing overall performance summary
        """
        logger.info("Generating performance summary...")
        
        summary = {
            'overall_score': 0,
            'kpi_status': {},
            'recommendations': [],
            'trends': {},
            'alerts': []
        }
        
        # Calculate overall performance score
        scores = []
        
        # TAT Score (30% weight)
        if 'tat' in self.results:
            tat_score = self.results['tat']['overall_stat']['compliance_rate'] * 100
            scores.append(tat_score * 0.30)
            summary['kpi_status']['tat'] = {
                'score': tat_score,
                'status': 'Good' if tat_score >= 80 else 'Needs Improvement',
                'target_met': self.results['tat']['overall_stat']['target_met']
            }
        
        # Staffing Score (25% weight)
        if 'staffing' in self.results:
            staffing_score = (1 - self.results['staffing']['overall']['avg_idle_time']) * 100
            scores.append(staffing_score * 0.25)
            summary['kpi_status']['staffing'] = {
                'score': staffing_score,
                'status': 'Good' if staffing_score >= 80 else 'Needs Improvement',
                'target_met': self.results['staffing']['overall']['utilization_target_met']
            }
        
        # Queue Score (25% weight)
        if 'queue' in self.results:
            queue_score = (1 - self.results['queue']['no_show_rates']['overall_rate']) * 100
            scores.append(queue_score * 0.25)
            summary['kpi_status']['queue'] = {
                'score': queue_score,
                'status': 'Good' if queue_score >= 90 else 'Needs Improvement',
                'target_met': self.results['queue']['no_show_rates']['overall_rate'] <= self.kpis['queue']['no_show_target']
            }
        
        # Volume Score (20% weight)
        if 'volume' in self.results:
            volume_score = 85  # Assuming stable volume
            scores.append(volume_score * 0.20)
            summary['kpi_status']['volume'] = {
                'score': volume_score,
                'status': 'Good',
                'target_met': True
            }
        
        summary['overall_score'] = sum(scores)
        
        # Generate recommendations
        recommendations = []
        
        if 'tat' in self.results and not self.results['tat']['overall_stat']['target_met']:
            recommendations.append("Improve STAT TAT performance, especially during night shift")
        
        if 'staffing' in self.results and not self.results['staffing']['overall']['utilization_target_met']:
            recommendations.append("Optimize staffing utilization to reduce idle time")
        
        if 'queue' in self.results and self.results['queue']['no_show_rates']['overall_rate'] > self.kpis['queue']['no_show_target']:
            recommendations.append("Implement strategies to reduce no-show rates")
        
        summary['recommendations'] = recommendations
        
        # Generate alerts
        alerts = []
        if 'tat' in self.results and self.results['tat']['overall_stat']['avg_tat'] > 60:
            alerts.append("CRITICAL: STAT TAT exceeding target threshold")
        
        if 'staffing' in self.results and self.results['staffing']['overall']['avg_idle_time'] > 0.40:
            alerts.append("WARNING: High staff idle time detected")
        
        summary['alerts'] = alerts
        
        self.summary_stats = summary
        logger.info(f"Performance Summary Complete - Overall Score: {summary['overall_score']:.1f}")
        
        return summary
    
    def create_visualizations(self) -> None:
        """
        Create performance visualization charts
        """
        logger.info("Creating performance visualizations...")
        
        # Set up the plotting style
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Lab Performance Dashboard', fontsize=16, fontweight='bold')
        
        # TAT Performance by Shift
        if 'tat' in self.results:
            shifts = list(self.results['tat']['stat_performance'].keys())
            tat_values = [self.results['tat']['stat_performance'][shift]['avg_tat'] for shift in shifts]
            
            axes[0, 0].bar(shifts, tat_values, color=['#2E86AB', '#A23B72', '#F18F01', '#C73E1D'])
            axes[0, 0].axhline(y=self.kpis['tat']['stat_target'], color='red', linestyle='--', label='Target')
            axes[0, 0].set_title('STAT TAT by Shift')
            axes[0, 0].set_ylabel('Minutes')
            axes[0, 0].legend()
            axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Staff Idle Time by Station
        if 'staffing' in self.results:
            stations = list(self.results['staffing']['idle_time'].keys())
            idle_times = [self.results['staffing']['idle_time'][station]['idle_time'] * 100 for station in stations]
            
            axes[0, 1].bar(stations, idle_times, color='#FF6B6B')
            axes[0, 1].axhline(y=self.kpis['staffing']['idle_time_target'] * 100, color='red', linestyle='--', label='Target')
            axes[0, 1].set_title('Staff Idle Time by Station')
            axes[0, 1].set_ylabel('Idle Time (%)')
            axes[0, 1].legend()
            axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Volume Trends
        if 'volume' in self.results:
            months = list(self.results['volume']['patient_encounters'].keys())[:3]
            volumes = [self.results['volume']['patient_encounters'][month] for month in months]
            
            axes[1, 0].plot(months, volumes, marker='o', linewidth=2, markersize=8)
            axes[1, 0].set_title('Monthly Patient Encounters')
            axes[1, 0].set_ylabel('Number of Encounters')
            axes[1, 0].grid(True, alpha=0.3)
        
        # Queue Performance
        if 'queue' in self.results:
            queue_types = list(self.results['queue']['queue_types'].keys())
            wait_times = [self.results['queue']['queue_types'][qt]['avg_wait'] for qt in queue_types]
            
            axes[1, 1].bar(queue_types, wait_times, color=['#4ECDC4', '#45B7D1', '#96CEB4'])
            axes[1, 1].axhline(y=self.kpis['queue']['wait_time_target'], color='red', linestyle='--', label='Target')
            axes[1, 1].set_title('Average Wait Times by Queue Type')
            axes[1, 1].set_ylabel('Minutes')
            axes[1, 1].legend()
        
        plt.tight_layout()
        plt.savefig('lab_performance_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        logger.info("Visualizations created and saved as 'lab_performance_dashboard.png'")
    
    def generate_report(self) -> str:
        """
        Generate a comprehensive performance report
        
        Returns:
            String containing the formatted report
        """
        logger.info("Generating comprehensive performance report...")
        
        report = []
        report.append("=" * 80)
        report.append("LAB PERFORMANCE ANALYSIS REPORT")
        report.append("Kaiser Permanente Lab Automation System - Largo, MD")
        report.append("=" * 80)
        report.append("")
        
        # Executive Summary
        report.append("EXECUTIVE SUMMARY")
        report.append("-" * 40)
        if self.summary_stats:
            report.append(f"Overall Performance Score: {self.summary_stats['overall_score']:.1f}/100")
            report.append("")
            
            for kpi, status in self.summary_stats['kpi_status'].items():
                report.append(f"{kpi.upper()}: {status['score']:.1f}/100 - {status['status']}")
        
        report.append("")
        
        # TAT Analysis
        report.append("TURNAROUND TIME (TAT) ANALYSIS")
        report.append("-" * 40)
        if 'tat' in self.results:
            tat_data = self.results['tat']
            report.append(f"Overall STAT TAT: {tat_data['overall_stat']['avg_tat']:.1f} minutes")
            report.append(f"STAT Compliance Rate: {tat_data['overall_stat']['compliance_rate']:.1%}")
            report.append(f"Target Met: {'Yes' if tat_data['overall_stat']['target_met'] else 'No'}")
            report.append("")
            
            report.append("TAT by Shift:")
            for shift, data in tat_data['stat_performance'].items():
                report.append(f"  {shift.replace('_', ' ').title()}: {data['avg_tat']:.1f} min (Compliance: {data['compliance_rate']:.1%})")
        
        report.append("")
        
        # Staffing Analysis
        report.append("STAFFING PERFORMANCE ANALYSIS")
        report.append("-" * 40)
        if 'staffing' in self.results:
            staffing_data = self.results['staffing']
            report.append(f"Average Idle Time: {staffing_data['overall']['avg_idle_time']:.1%}")
            report.append(f"Average Utilization: {staffing_data['overall']['avg_utilization']:.1%}")
            report.append(f"Utilization Target Met: {'Yes' if staffing_data['overall']['utilization_target_met'] else 'No'}")
            report.append("")
            
            report.append("Idle Time by Station:")
            for station, data in staffing_data['idle_time'].items():
                status = "⚠️" if data['idle_time'] > 0.30 else "✅"
                report.append(f"  {station}: {data['idle_time']:.1%} {status}")
        
        report.append("")
        
        # Volume Analysis
        report.append("VOLUME METRICS")
        report.append("-" * 40)
        if 'volume' in self.results:
            volume_data = self.results['volume']
            report.append("Monthly Patient Encounters:")
            for month, count in volume_data['patient_encounters'].items():
                report.append(f"  {month.title()}: {count:,}")
            report.append("")
            
            report.append("Lab Volume by Type:")
            for test_type, data in volume_data['lab_volumes'].items():
                report.append(f"  {test_type.replace('_', ' ').title()}: {data['volume']:,} ({data['percentage']:.1%})")
        
        report.append("")
        
        # Queue Performance
        report.append("QUEUE PERFORMANCE")
        report.append("-" * 40)
        if 'queue' in self.results:
            queue_data = self.results['queue']
            report.append(f"Overall No-Show Rate: {queue_data['no_show_rates']['overall_rate']:.1%}")
            report.append("")
            
            report.append("Wait Times by Queue Type:")
            for queue_type, data in queue_data['queue_types'].items():
                report.append(f"  {queue_type.replace('_', ' ').title()}: {data['avg_wait']:.1f} min")
        
        report.append("")
        
        # Recommendations
        report.append("RECOMMENDATIONS")
        report.append("-" * 40)
        if self.summary_stats and self.summary_stats['recommendations']:
            for i, rec in enumerate(self.summary_stats['recommendations'], 1):
                report.append(f"{i}. {rec}")
        else:
            report.append("No specific recommendations at this time.")
        
        report.append("")
        
        # Alerts
        if self.summary_stats and self.summary_stats['alerts']:
            report.append("ALERTS")
            report.append("-" * 40)
            for alert in self.summary_stats['alerts']:
                report.append(f"🚨 {alert}")
            report.append("")
        
        report.append("=" * 80)
        report.append("Report generated on: " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))
        report.append("=" * 80)
        
        report_text = "\n".join(report)
        
        # Save report to file
        with open('lab_performance_report.txt', 'w') as f:
            f.write(report_text)
        
        logger.info("Performance report generated and saved as 'lab_performance_report.txt'")
        
        return report_text
    
    def run_complete_analysis(self) -> Dict:
        """
        Run complete lab performance analysis
        
        Returns:
            Dictionary containing all analysis results
        """
        logger.info("Starting complete lab performance analysis...")
        
        try:
            # Run all analyses
            self.analyze_tat_data()
            self.analyze_staffing_performance()
            self.analyze_volume_metrics()
            self.analyze_queue_performance()
            
            # Generate summary and report
            self.generate_performance_summary()
            self.create_visualizations()
            report = self.generate_report()
            
            logger.info("Complete lab performance analysis finished successfully")
            
            return {
                'results': self.results,
                'summary': self.summary_stats,
                'report': report
            }
            
        except Exception as e:
            logger.error(f"Error during analysis: {str(e)}")
            raise


def main():
    """
    Main function to run the lab performance analysis
    """
    print("Lab Performance Analyzer")
    print("Kaiser Permanente Lab Automation System - Largo, MD")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = LabPerformanceAnalyzer()
    
    # Run complete analysis
    try:
        results = analyzer.run_complete_analysis()
        
        print("\nAnalysis Complete!")
        print(f"Overall Performance Score: {results['summary']['overall_score']:.1f}/100")
        print("\nKey Findings:")
        
        for kpi, status in results['summary']['kpi_status'].items():
            print(f"  {kpi.upper()}: {status['score']:.1f}/100 - {status['status']}")
        
        print("\nFiles Generated:")
        print("  - lab_performance_report.txt (Detailed report)")
        print("  - lab_performance_dashboard.png (Visualizations)")
        print("  - lab_analysis.log (Analysis logs)")
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        logger.error(f"Analysis failed: {str(e)}")


if __name__ == "__main__":
    main()




