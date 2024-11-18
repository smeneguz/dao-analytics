import os
import shutil
import zipfile
import kagglehub
import pandas as pd
from typing import Dict, Optional, List
from pathlib import Path
import logging

class DataLoader:
    def __init__(self, 
                 kaggle_dataset: str = "daviddavo/dao-analyzer", 
                 local_path: Optional[str] = None,
                 data_dir: str = "data"):
        """
        Initialize DataLoader with Kaggle dataset information.
        
        Args:
            kaggle_dataset: Kaggle dataset path in format "username/dataset-name"
            local_path: Optional local path to use instead of downloading
            data_dir: Directory where data will be stored/extracted
        """
        self.kaggle_dataset = kaggle_dataset
        self.local_path = local_path
        self.data_dir = data_dir
        self.logger = logging.getLogger(__name__)
        self.data_paths = {}

    def extract_zip(self, zip_path: str, extract_path: str) -> None:
        """Extract zip file to specified path."""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            self.logger.info(f"Successfully extracted files to {extract_path}")
        except Exception as e:
            self.logger.error(f"Error extracting zip file: {str(e)}")
            raise

    def setup_data_directory(self) -> str:
        """Set up and return path to data directory."""
        try:
            # If local path is specified and exists, use it
            if self.local_path and os.path.exists(self.local_path):
                self.logger.info(f"Using local data path: {self.local_path}")
                return self.local_path

            # Create data directory if it doesn't exist
            os.makedirs(self.data_dir, exist_ok=True)

            # Download dataset from Kaggle
            self.logger.info("Downloading dataset from Kaggle...")
            downloaded_path = kagglehub.dataset_download(self.kaggle_dataset)
            
            # Check if downloaded_path is a zip file
            if os.path.isfile(downloaded_path) and downloaded_path.endswith('.zip'):
                extract_dir = os.path.join(self.data_dir, 'extracted')
                self.extract_zip(downloaded_path, extract_dir)
                
                # Find the main data directory in the extracted contents
                extracted_contents = os.listdir(extract_dir)
                if extracted_contents:
                    # Use the first directory as the main data directory
                    data_path = os.path.join(extract_dir, extracted_contents[0])
                    self.logger.info(f"Using extracted data path: {data_path}")
                    return data_path
            else:
                # If it's already a directory, use it directly
                self.logger.info(f"Using downloaded data path: {downloaded_path}")
                return downloaded_path

        except Exception as e:
            self.logger.error(f"Error setting up data directory: {str(e)}")
            raise

    def find_csv_files(self, directory: str) -> Dict[str, str]:
        """Recursively find all CSV files in the directory and subdirectories."""
        if directory in self.data_paths:
            return self.data_paths[directory]

        csv_files = {}
        try:
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith('.csv'):
                        # Create a friendly name based on the directory structure
                        rel_path = os.path.relpath(root, directory)
                        friendly_name = os.path.join(rel_path, Path(file).stem).replace('/', '_')
                        full_path = os.path.join(root, file)
                        csv_files[friendly_name] = full_path
                        self.logger.debug(f"Found CSV file: {friendly_name} at {full_path}")

            self.data_paths[directory] = csv_files
            return csv_files
        except Exception as e:
            self.logger.error(f"Error scanning directory {directory}: {str(e)}")
            raise

    def load_csv(self, filepath: str) -> pd.DataFrame:
        """Load a CSV file and return as DataFrame."""
        try:
            df = pd.read_csv(filepath, header=0)
            self.logger.debug(f"Successfully loaded {filepath}")
            return df
        except Exception as e:
            self.logger.error(f"Error loading {filepath}: {str(e)}")
            raise

    def get_available_datasets(self) -> Dict[str, pd.DataFrame]:
        """Load all available CSV files and return them as a dictionary of DataFrames."""
        # Set up data directory and get path
        data_path = self.setup_data_directory()
        
        # Find all CSV files
        csv_files = self.find_csv_files(data_path)
        
        # Load each CSV file
        datasets = {}
        for name, path in csv_files.items():
            try:
                datasets[name] = self.load_csv(path)
                self.logger.info(f"Successfully loaded dataset: {name}")
            except Exception as e:
                self.logger.warning(f"Skipping {name} due to error: {str(e)}")
                continue
                
        return datasets

    def cleanup_downloaded_data(self):
        """Clean up downloaded and extracted data."""
        try:
            if os.path.exists(self.data_dir):
                shutil.rmtree(self.data_dir)
                self.logger.info(f"Cleaned up {self.data_dir}")
        except Exception as e:
            self.logger.error(f"Error cleaning up data directory: {str(e)}")