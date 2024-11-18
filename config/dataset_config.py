DATASET_CONFIGS = {
    'active_daos': {
        'required_columns': ['createdAt', 'id'],
        'date_column': 'createdAt',
        'aggregation': 'monthly',
        'metrics': ['count', 'cumulative_sum']
    },
    'users': {
        'required_columns': ['createdAt', 'address'],
        'date_column': 'createdAt',
        'aggregation': 'monthly',
        'metrics': ['unique_count', 'cumulative_sum']
    },
    'transactions': {
        'required_columns': ['date', 'amount', 'token'],
        'date_column': 'date',
        'aggregation': 'daily',
        'metrics': ['sum', 'average', 'count']
    }
}

VISUALIZATION_CONFIGS = {
    'active_daos': {
        'plot_type': 'line',
        'title': 'Active DAOs Over Time',
        'x_label': 'Date',
        'y_label': 'Number of DAOs'
    },
    'users': {
        'plot_type': 'line',
        'title': 'User Growth Over Time',
        'x_label': 'Date',
        'y_label': 'Number of Users'
    },
    'transactions': {
        'plot_type': 'bar',
        'title': 'Transaction Volume Over Time',
        'x_label': 'Date',
        'y_label': 'Volume'
    }
}