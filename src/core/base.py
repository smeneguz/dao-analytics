from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import pandas as pd

class DatasetProvider(ABC):
    """Abstract base class for dataset providers"""
    @abstractmethod
    def get_datasets(self) -> Dict[str, pd.DataFrame]:
        """Retrieve all datasets from the provider"""
        pass

    @abstractmethod
    def get_version_info(self) -> Dict[str, Any]:
        """Get version information about the datasets"""
        pass

class DataProcessor(ABC):
    """Abstract base class for data processors"""
    @abstractmethod
    def process(self, df: pd.DataFrame, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Process a dataset and return results"""
        pass

class Analyzer(ABC):
    """Abstract base class for data analyzers"""
    @abstractmethod
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze processed data and return results"""
        pass

class Visualizer(ABC):
    """Abstract base class for data visualizers"""
    @abstractmethod
    def visualize(self, data: Dict[str, Any]) -> Any:
        """Create visualization from analyzed data"""
        pass