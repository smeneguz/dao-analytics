from typing import Dict, Any

class PlotConfig:
    DATE_FORMAT = '%b, %Y'

    @staticmethod
    def get_base_layout(dates: list) -> Dict[str, Any]:
        """Get base layout configuration for plots."""
        return {
            'xaxis': {
                'tickvals': dates,
                'tickformat': PlotConfig.DATE_FORMAT,
                'tickangle': 45,
                'ticks': 'outside',
                'ticklen': 5,
                'tickwidth': 2,
                'showline': True,
                'linewidth': 2,
                'linecolor': 'black',
                'tickfont': {'size': 14},
            },
            'yaxis': {
                'showgrid': True,
                'gridwidth': 0.5,
                'gridcolor': '#B0BEC5',
                'ticks': 'outside',
                'ticklen': 5,
                'tickwidth': 2,
                'showline': True,
                'linewidth': 2,
                'linecolor': 'black',
                'tickfont': {'size': 12},
                'tick0': 0,
                'dtick': 100,
            },
            'plot_bgcolor': "white",
            'legend': {'orientation': 'h', 'x': 0, 'y': 1.2}
        }

    PLATFORM_STYLES = {
        'daostack_mainnet': {
            'color': '#A5D6A7',
            'symbol': 'circle-open',
        },
        'daostack_xdai': {
            'color': '#388E3C',
            'symbol': 'circle',
        },
        'daohaus_mainnet': {
            'color': '#FFCC80',
            'symbol': 'diamond-tall-open',
        },
        'daohaus_xdai': {
            'color': '#F57C00',
            'symbol': 'diamond-tall',
        },
        'aragon_mainnet': {
            'color': '#90CAF9',
            'symbol': 'x-open',
        },
        'aragon_xdai': {
            'color': '#1976D2',
            'symbol': 'x',
        }
    }