# DAO Analyzer

A Python tool for analyzing and comparing Decentralized Autonomous Organizations (DAOs) data across different platforms.

## Features

- Downloads and processes DAO data from multiple sources
- Provides comprehensive analysis of DAO metrics
- Temporal analysis of DAO activities
- Network analysis of DAO relationships
- Data backup and version control
- Extensible architecture for adding new data sources

## Installation

```bash
git clone https://github.com/yourusername/dao-analyzer.git
cd dao-analyzer
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```python
from src.providers.kaggle_provider import KaggleDatasetProvider
from src.processors.dao_processor import DAODataProcessor
from src.analyzers.dao_analyzer import DAOAnalyzer

# Initialize components
provider = KaggleDatasetProvider("daviddavo/dao-analyzer")
processor = DAODataProcessor()
analyzer = DAOAnalyzer()

# Get and analyze data
datasets = provider.get_datasets()
processed_data = {name: processor.process(df) for name, df in datasets.items()}
analysis = analyzer.analyze(processed_data)
```

## Project Structure

```
dao-analyzer/
├── src/
│   ├── core/           # Core functionality and base classes
│   ├── providers/      # Data providers (Kaggle, etc.)
│   ├── processors/     # Data processing modules
│   └── analyzers/      # Analysis modules
├── data/              # Data storage
│   └── backup/        # Backup storage
├── tests/            # Test files
└── requirements.txt  # Project dependencies
```

## Data Sources

Currently supports:
- Aragon
- DAOstack
- DAOhaus

## Requirements

- Python 3.7+
- pandas
- kagglehub
- plotly

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License

## Authors

Your Name - Initial work

## Acknowledgments

- Arroyo, Javier, Davó, David, & Faqir-Rhazoui, Youssef. (2023). DAO Analyzer dataset [Data set]. Zenodo. https://doi.org/10.5281/zenodo.7669709
- The DAO research community