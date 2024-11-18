from typing import Dict, Any

# Assuming DataProcessor is defined in a module named data_processor_base
from src.utils.data_processing import DataProcessor
import pandas as pd
from datetime import datetime
import numpy as np
import logging


class DAODataProcessor(DataProcessor):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    """Processes DAO-related datasets with various metrics"""
    
    def process(self, df: pd.DataFrame, metadata: Dict[str, Any]) -> Dict[str, Any]:
        dataset_name = metadata.get('name', '')
        results = {
            'dataset_name': dataset_name,
            'record_count': len(df),
            'columns': df.columns.tolist(),
            'summary': self._get_summary_stats(df),
            'temporal_analysis': self._get_temporal_analysis(df),
            'network_stats': self._get_network_stats(df)
        }
        
        if 'date' in results['temporal_analysis']:
            results['time_series'] = self._get_time_series_analysis(
                df, 
                results['temporal_analysis']['date_column']
            )
        
        return results

    def _get_summary_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get basic summary statistics for the dataset"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        return {
            'numeric_stats': df[numeric_cols].describe().to_dict() if len(numeric_cols) > 0 else {},
            'missing_values': df.isnull().sum().to_dict(),
            'unique_values': {col: df[col].nunique() for col in df.columns}
        }

    def _get_temporal_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Identify and analyze temporal aspects of the data"""
        date_columns = []
        date_column = None
        
        for col in df.columns:
            try:
                # First try to convert numeric timestamps
                if pd.api.types.is_numeric_dtype(df[col]):
                    pd.to_datetime(df[col], unit='s')
                    date_columns.append(col)
                    date_column = col
                    break
                # Then try string dates
                elif pd.api.types.is_string_dtype(df[col]):
                    pd.to_datetime(df[col])
                    date_columns.append(col)
                    date_column = col
                    break
            except:
                continue
        
        if date_column:
            return {
                'has_temporal_data': True,
                'date_columns': date_columns,
                'date_column': date_column
            }
        
        return {'has_temporal_data': False}

    def _get_network_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get network-related statistics if applicable"""
        network_stats = {}
        
        # Check for network/address columns
        address_columns = [col for col in df.columns if 'address' in col.lower()]
        if address_columns:
            network_stats['address_columns'] = {
                col: df[col].nunique() for col in address_columns
            }
        
        # Check for network type if present
        if 'network' in df.columns:
            network_stats['networks'] = df['network'].value_counts().to_dict()
            
        return network_stats

    def _get_time_series_analysis(self, df: pd.DataFrame, date_column: str) -> Dict[str, Any]:
        """Perform time series analysis on temporal data"""
        try:
            # Convert to datetime based on column type
            if pd.api.types.is_numeric_dtype(df[date_column]):
                dates = pd.to_datetime(df[date_column].astype(float), unit='s')
            else:
                dates = pd.to_datetime(df[date_column])
            
            # Group by month
            monthly = pd.DataFrame({'date': dates}).resample('M', on='date').size()
            
            return {
                'monthly_activity': monthly.to_dict(),
                'total_months': len(monthly),
                'start_date': dates.min().isoformat(),
                'end_date': dates.max().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error in time series analysis: {str(e)}")
            return {'error': str(e)}
