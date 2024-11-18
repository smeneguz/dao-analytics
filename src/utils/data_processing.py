import logging
import pandas as pd
from datetime import date
from pandas.tseries.offsets import DateOffset
from typing import List, Optional, Dict

class DataProcessor:
    DATE_COLUMNS = ['createdAt', 'date', 'startDate', 'executedAt']
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def identify_date_column(self, df: pd.DataFrame) -> str:
        """Identify which date column is present in the DataFrame."""
        for col in self.DATE_COLUMNS:
            if col in df.columns:
                return col
        raise ValueError("No recognized date column found in DataFrame")

    def convert_timestamp(self, value, unit='s'):
        """Convert timestamp to datetime handling different formats."""
        try:
            if pd.isna(value):
                return None
            if isinstance(value, (int, float)):
                return pd.to_datetime(value, unit=unit)
            return pd.to_datetime(value)
        except Exception as e:
            self.logger.error(f"Error converting timestamp {value}: {str(e)}")
            return None

    def process_dataset(self, df: pd.DataFrame, dataset_name: str) -> Optional[pd.DataFrame]:
        """Process a dataset based on its name and content."""
        try:
            date_key = self.identify_date_column(df)
            return self.process_new_daos(df, date_key)
        except Exception as e:
            self.logger.error(f"Error processing dataset {dataset_name}: {str(e)}")
            return None

    def process_new_daos(self, df: pd.DataFrame, date_key: str) -> pd.DataFrame:
        """Process DAO data to get new DAOs per month."""
        dff = df.copy()
        
        # Convert timestamp to datetime
        dff[date_key] = dff[date_key].apply(lambda x: self.convert_timestamp(x))
        dff = dff.dropna(subset=[date_key])
        
        # Convert to date and set to first of month
        dff[date_key] = dff[date_key].dt.date
        dff[date_key] = dff[date_key].apply(lambda d: d.replace(day=1))

        # Group by date and count
        dff = dff.groupby([date_key]).size().reset_index(name='count')

        # Generate complete time series
        today = date.today().replace(day=1)
        start = dff[date_key].min()
        idx = pd.date_range(start=start, end=today, freq=DateOffset(months=1))

        # Create complete timeline
        df_complete = pd.DataFrame({
            date_key: idx.date,
            'count': 0
        })

        # Merge with actual data
        dff = pd.concat([dff, df_complete]).drop_duplicates(subset=date_key, keep="first")
        return dff.sort_values(date_key)

    def calculate_cumulative_total(self, values: List[float]) -> List[float]:
        """Calculate cumulative total from a list of values."""
        return [sum(values[:i+1]) for i in range(len(values))]
