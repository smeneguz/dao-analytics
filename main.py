import logging
from pathlib import Path
from src.providers.kaggle_provider import KaggleDatasetProvider
from src.processors.dao_processor import DAODataProcessor
from src.analyzers.dao_analyzer import DAOAnalyzer

def setup_logging():
    """Set up logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        # Initialize components
        provider = KaggleDatasetProvider(
            dataset_path="daviddavo/dao-analyzer",
            backup_dir=Path("data/backup")
        )
        
        # Print dataset version info
        version_info = provider.get_version_info()
        print("\nDataset Information:")
        for key, value in version_info.items():
            print(f"{key}: {value}")
            
        # Get and process datasets
        processor = DAODataProcessor()
        analyzer = DAOAnalyzer()
        
        # Load datasets
        datasets = provider.get_datasets()
        logger.info(f"Loaded {len(datasets)} datasets")
        
        # Process each dataset
        processed_data = {}
        for name, df in datasets.items():
            logger.info(f"Processing {name}")
            processed_data[name] = processor.process(df, {'name': name})
        
        # Analyze processed data
        analysis_results = analyzer.analyze(processed_data)
        
        # Display results
        print("\nAnalysis Results:")
        for dataset, metrics in analysis_results['dataset_metrics'].items():
            print(f"\n{dataset}:")
            print(f"Records: {metrics['record_count']}")
            print(f"Completeness: {metrics['completeness']:.2%}")
            
            if dataset in analysis_results['temporal_metrics']:
                temporal = analysis_results['temporal_metrics'][dataset]
                print(f"Time span: {temporal['time_span']}")
                if 'trend' in temporal['activity_trend']:
                    print(f"Activity trend: {temporal['activity_trend']['trend']}")

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()
