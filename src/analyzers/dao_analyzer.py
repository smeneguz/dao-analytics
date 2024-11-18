from src.core.base import Analyzer
from typing import Dict, Any
import pandas as pd

class DAOAnalyzer(Analyzer):
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze processed DAO data and compute metrics"""
        analysis = {
            'dataset_metrics': {},
            'temporal_metrics': {},
            'network_metrics': {},
            'cross_dataset_metrics': {}
        }
        
        for dataset_name, dataset_data in data.items():
            # Dataset-specific metrics
            analysis['dataset_metrics'][dataset_name] = {
                'record_count': dataset_data['record_count'],
                'column_count': len(dataset_data['columns']),
                'completeness': self._calculate_completeness(dataset_data)
            }
            
            # Temporal metrics if available
            if 'time_series' in dataset_data:
                analysis['temporal_metrics'][dataset_name] = {
                    'activity_trend': self._calculate_trend(dataset_data['time_series']),
                    'time_span': self._calculate_timespan(dataset_data['time_series'])
                }
            
            # Network metrics if available
            if dataset_data['network_stats']:
                analysis['network_metrics'][dataset_name] = {
                    'network_distribution': dataset_data['network_stats'].get('networks', {}),
                    'unique_addresses': self._count_unique_addresses(dataset_data)
                }
        
        # Add cross-dataset analysis
        analysis['cross_dataset_metrics'] = self._analyze_cross_dataset_relationships(data)
        
        return analysis
    
    def _count_unique_addresses(self, data: Dict) -> int:
        """Count unique addresses across all address columns"""
        try:
            if 'network_stats' not in data or 'address_columns' not in data['network_stats']:
                return 0
            return sum(data['network_stats']['address_columns'].values())
        except Exception as e:
            self.logger.error(f"Error counting addresses: {str(e)}")
            return 0
        
    def _calculate_timespan(self, time_series: Dict) -> str:
        """Calculate the timespan between start and end dates"""
        try:
            if 'start_date' not in time_series or 'end_date' not in time_series:
                return "Unknown"
            return f"{time_series['start_date']} to {time_series['end_date']}"
        except Exception as e:
            self.logger.error(f"Error calculating timespan: {str(e)}")
            return "Unknown"

    def _calculate_completeness(self, data: Dict) -> float:
        """Calculate data completeness score"""
        if 'summary' not in data:
            return 0.0
        
        missing = sum(data['summary']['missing_values'].values())
        total = data['record_count'] * len(data['columns'])
        return 1 - (missing / total) if total > 0 else 0
    
    def _analyze_cross_dataset_relationships(self, data: Dict) -> Dict[str, Any]:
        """Analyze relationships between datasets"""
        return {
            'total_datasets': len(data),
            'datasets_with_temporal_data': sum(1 for d in data.values() if 'time_series' in d),
            'datasets_with_network_data': sum(1 for d in data.values() if d.get('network_stats'))
        }

    def _calculate_trend(self, time_series: Dict) -> Dict[str, Any]:
        """Calculate activity trends from time series data"""
        if 'monthly_activity' not in time_series:
            return {}
            
        activity = pd.Series(time_series['monthly_activity'])
        return {
            'trend': 'increasing' if activity.is_monotonic_increasing else 
                    'decreasing' if activity.is_monotonic_decreasing else 'varying',
            'peak_month': activity.idxmax().isoformat(),
            'peak_value': float(activity.max())
        }