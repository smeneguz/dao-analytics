from src.core.base import DatasetProvider
import kagglehub
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import pandas as pd
import logging
import json

class KaggleDatasetProvider(DatasetProvider):
    def __init__(self, dataset_path: str, backup_dir: Path):
        self.dataset_path = dataset_path
        self.backup_dir = backup_dir
        self.logger = logging.getLogger(__name__)
        self._version_info = None
        
    def get_version_info(self) -> Dict[str, Any]:
        if not self._version_info:
            try:
                path = kagglehub.dataset_download(self.dataset_path)
                version = path.split('versions/')[-1]
                self._version_info = {
                    'source': 'kaggle',
                    'dataset': self.dataset_path,
                    'version': version,
                    'download_date': datetime.now().isoformat(),
                    'path': path
                }
                self._save_version_info()
            except Exception as e:
                self.logger.warning(f"Failed to get Kaggle version: {e}")
                self._version_info = self._load_backup_version()
        
        return self._version_info

    def get_datasets(self) -> Dict[str, pd.DataFrame]:
        version_info = self.get_version_info()
        data_path = Path(version_info['path'])
        
        datasets = {}
        for csv_file in data_path.rglob('*.csv'):
            try:
                dataset_name = csv_file.stem
                datasets[dataset_name] = pd.read_csv(csv_file)
                self.logger.info(f"Loaded dataset: {dataset_name}")
            except Exception as e:
                self.logger.error(f"Error loading {csv_file}: {e}")
        
        return datasets

    def _save_version_info(self):
        version_file = self.backup_dir / 'version_info.json'
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        with open(version_file, 'w') as f:
            json.dump(self._version_info, f)

    def _load_backup_version(self) -> Dict[str, Any]:
        version_file = self.backup_dir / 'version_info.json'
        if version_file.exists():
            with open(version_file) as f:
                return json.load(f)
        return {}
