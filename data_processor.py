#!/usr/bin/env python3
"""
Data Processor for Lab Performance Analysis
Handles large CSV files and extracts key performance metrics

Author: Lab Operations Manager
Date: 2024
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class LabDataProcessor:
    """
    Processes lab performance data from various file formats
    """
    
    def __init__(self, data_path: str = "data"):
        """
        Initialize the data processor
        
        Args:
            data_path: Path to the data directory
        """
        self.data_path = Path(data_path)
        self.processed_data = {}
        
    def process_csv_data(self, filename: str = "STAT TAT- Summary_Full Data_data.csv") -> Dict:
        """
        Process the large CSV file in chunks to extract key metrics
        
        Args:
            filename: Name of the CSV file to process
            
        Returns:
            Dictionary containing processed data
        """
        logger.info(f"Processing CSV file: {filename}")
        
        csv_path = self.data_path / filename
        
        if not csv_path.exists():
            logger.warning(f"CSV file not found: {csv_path}")
            return {}
        
        try:
            # Read CSV in chunks to handle large file
            chunk_size = 10000
            chunks = []
            
            # Read first few rows to understand structure
            sample_df = pd.read_csv(csv_path, nrows=100)
            logger.info(f"CSV columns: {list(sample_df.columns)}")
            
            # Process in chunks
            for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
                chunks.append(chunk)
            
            # Combine chunks
            df = pd.concat(chunks, ignore_index=True)
            logger.info(f"Total rows processed: {len(df)}")
            
            # Extract key metrics based on column names
            metrics = self._extract_metrics_from_dataframe(df)
            
            self.processed_data['csv_metrics'] = metrics
            return metrics
            
        except Exception as e:
            logger.error(f"Error processing CSV file: {str(e)}")
            return {}
    
    def _extract_metrics_from_dataframe(self, df: pd.DataFrame) -> Dict:
        """
        Extract key metrics from the processed dataframe
        
        Args:
            df: Processed dataframe
            
        Returns:
            Dictionary containing extracted metrics
        """
        metrics = {
            'summary_stats': {},
            'tat_analysis': {},
            'volume_analysis': {},
            'trends': {}
        }
        
        # Basic summary statistics
        metrics['summary_stats'] = {
            'total_records': len(df),
            'date_range': self._get_date_range(df),
            'unique_patients': self._get_unique_count(df, 'patient_id'),
            'unique_tests': self._get_unique_count(df, 'test_type')
        }
        
        # TAT Analysis (if TAT columns exist)
        tat_columns = [col for col in df.columns if 'tat' in col.lower() or 'turnaround' in col.lower()]
        if tat_columns:
            metrics['tat_analysis'] = self._analyze_tat_columns(df, tat_columns)
        
        # Volume Analysis
        volume_columns = [col for col in df.columns if 'volume' in col.lower() or 'count' in col.lower()]
        if volume_columns:
            metrics['volume_analysis'] = self._analyze_volume_columns(df, volume_columns)
        
        # Time-based trends
        time_columns = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
        if time_columns:
            metrics['trends'] = self._analyze_time_trends(df, time_columns)
        
        return metrics
    
    def _get_date_range(self, df: pd.DataFrame) -> Dict:
        """Extract date range from dataframe"""
        date_columns = [col for col in df.columns if 'date' in col.lower()]
        if date_columns:
            try:
                date_col = date_columns[0]
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                min_date = df[date_col].min()
                max_date = df[date_col].max()
                return {
                    'start_date': min_date.strftime('%Y-%m-%d') if pd.notna(min_date) else 'Unknown',
                    'end_date': max_date.strftime('%Y-%m-%d') if pd.notna(max_date) else 'Unknown',
                    'duration_days': (max_date - min_date).days if pd.notna(min_date) and pd.notna(max_date) else 0
                }
            except:
                return {'start_date': 'Unknown', 'end_date': 'Unknown', 'duration_days': 0}
        return {'start_date': 'Unknown', 'end_date': 'Unknown', 'duration_days': 0}
    
    def _get_unique_count(self, df: pd.DataFrame, column_name: str) -> int:
        """Get unique count for a column"""
        if column_name in df.columns:
            return df[column_name].nunique()
        return 0
    
    def _analyze_tat_columns(self, df: pd.DataFrame, tat_columns: List[str]) -> Dict:
        """Analyze TAT-related columns"""
        tat_analysis = {}
        
        for col in tat_columns:
            if col in df.columns:
                # Convert to numeric, handling non-numeric values
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
                tat_analysis[col] = {
                    'mean': df[col].mean(),
                    'median': df[col].median(),
                    'std': df[col].std(),
                    'min': df[col].min(),
                    'max': df[col].max(),
                    'p95': df[col].quantile(0.95),
                    'p99': df[col].quantile(0.99),
                    'null_count': df[col].isnull().sum(),
                    'total_count': len(df[col])
                }
        
        return tat_analysis
    
    def _analyze_volume_columns(self, df: pd.DataFrame, volume_columns: List[str]) -> Dict:
        """Analyze volume-related columns"""
        volume_analysis = {}
        
        for col in volume_columns:
            if col in df.columns:
                # Convert to numeric, handling non-numeric values
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
                volume_analysis[col] = {
                    'total': df[col].sum(),
                    'mean': df[col].mean(),
                    'median': df[col].median(),
                    'std': df[col].std(),
                    'min': df[col].min(),
                    'max': df[col].max(),
                    'null_count': df[col].isnull().sum(),
                    'total_count': len(df[col])
                }
        
        return volume_analysis
    
    def _analyze_time_trends(self, df: pd.DataFrame, time_columns: List[str]) -> Dict:
        """Analyze time-based trends"""
        trends = {}
        
        for col in time_columns:
            if col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    
                    # Group by date and count
                    daily_counts = df.groupby(df[col].dt.date).size()
                    
                    trends[col] = {
                        'daily_average': daily_counts.mean(),
                        'daily_std': daily_counts.std(),
                        'peak_day': daily_counts.idxmax().strftime('%Y-%m-%d') if len(daily_counts) > 0 else 'Unknown',
                        'peak_count': daily_counts.max(),
                        'total_days': len(daily_counts)
                    }
                except:
                    trends[col] = {'error': 'Could not parse time data'}
        
        return trends
    
    def analyze_file_structure(self) -> Dict:
        """
        Analyze the structure of all data files
        
        Returns:
            Dictionary containing file structure analysis
        """
        logger.info("Analyzing file structure...")
        
        file_analysis = {
            'pdf_files': [],
            'csv_files': [],
            'docx_files': [],
            'file_categories': {}
        }
        
        # Categorize files by type and content
        for file_path in self.data_path.glob('*'):
            if file_path.is_file():
                file_info = {
                    'name': file_path.name,
                    'size_mb': file_path.stat().st_size / (1024 * 1024),
                    'path': str(file_path)
                }
                
                if file_path.suffix.lower() == '.pdf':
                    file_analysis['pdf_files'].append(file_info)
                elif file_path.suffix.lower() == '.csv':
                    file_analysis['csv_files'].append(file_info)
                elif file_path.suffix.lower() == '.docx':
                    file_analysis['docx_files'].append(file_info)
        
        # Categorize by content based on filename
        categories = {
            'tat_reports': [],
            'staffing_reports': [],
            'volume_reports': [],
            'performance_reports': [],
            'queue_reports': []
        }
        
        for file_info in file_analysis['pdf_files'] + file_analysis['csv_files'] + file_analysis['docx_files']:
            filename = file_info['name'].lower()
            
            if 'tat' in filename or 'turnaround' in filename:
                categories['tat_reports'].append(file_info)
            elif 'staff' in filename or 'idle' in filename or 'performance' in filename:
                categories['staffing_reports'].append(file_info)
            elif 'volume' in filename or 'encounter' in filename:
                categories['volume_reports'].append(file_info)
            elif 'queue' in filename or 'wait' in filename:
                categories['queue_reports'].append(file_info)
            elif 'performance' in filename:
                categories['performance_reports'].append(file_info)
        
        file_analysis['file_categories'] = categories
        
        logger.info(f"Found {len(file_analysis['pdf_files'])} PDF files, {len(file_analysis['csv_files'])} CSV files")
        
        return file_analysis
    
    def generate_data_summary(self) -> str:
        """
        Generate a summary of the data files
        
        Returns:
            String containing the data summary
        """
        file_analysis = self.analyze_file_structure()
        
        summary = []
        summary.append("LAB DATA SUMMARY")
        summary.append("=" * 50)
        summary.append("")
        
        # File counts
        summary.append("FILE OVERVIEW:")
        summary.append(f"  PDF Files: {len(file_analysis['pdf_files'])}")
        summary.append(f"  CSV Files: {len(file_analysis['csv_files'])}")
        summary.append(f"  DOCX Files: {len(file_analysis['docx_files'])}")
        summary.append("")
        
        # Categories
        summary.append("REPORT CATEGORIES:")
        for category, files in file_analysis['file_categories'].items():
            summary.append(f"  {category.replace('_', ' ').title()}: {len(files)} files")
        summary.append("")
        
        # Key files
        summary.append("KEY DATA FILES:")
        for file_info in file_analysis['csv_files']:
            summary.append(f"  {file_info['name']} ({file_info['size_mb']:.1f} MB)")
        
        summary.append("")
        summary.append("NOTABLE REPORTS:")
        for category, files in file_analysis['file_categories'].items():
            if files:
                summary.append(f"  {category.replace('_', ' ').title()}:")
                for file_info in files[:3]:  # Show first 3 files
                    summary.append(f"    - {file_info['name']}")
                if len(files) > 3:
                    summary.append(f"    ... and {len(files) - 3} more")
                summary.append("")
        
        return "\n".join(summary)


def main():
    """
    Main function to run the data processor
    """
    print("Lab Data Processor")
    print("=" * 40)
    
    processor = LabDataProcessor()
    
    # Generate data summary
    summary = processor.generate_data_summary()
    print(summary)
    
    # Try to process CSV data
    print("\n" + "=" * 40)
    print("PROCESSING CSV DATA")
    print("=" * 40)
    
    try:
        csv_metrics = processor.process_csv_data()
        if csv_metrics:
            print("CSV Processing Results:")
            print(f"  Total Records: {csv_metrics.get('summary_stats', {}).get('total_records', 'Unknown')}")
            print(f"  Date Range: {csv_metrics.get('summary_stats', {}).get('date_range', {})}")
            
            if 'tat_analysis' in csv_metrics:
                print(f"  TAT Columns Found: {len(csv_metrics['tat_analysis'])}")
            
            if 'volume_analysis' in csv_metrics:
                print(f"  Volume Columns Found: {len(csv_metrics['volume_analysis'])}")
        else:
            print("No CSV data processed")
    except Exception as e:
        print(f"Error processing CSV: {str(e)}")


if __name__ == "__main__":
    main()



