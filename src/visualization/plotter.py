import plotly.graph_objects as go
from typing import Dict
import logging

class DAOPlotter:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create_scatter_trace(self, x_data, y_data, name: str) -> go.Scatter:
        return go.Scatter(
            x=x_data,
            y=y_data,
            name=name,
            mode='lines+markers'
        )

    def create_plots(self, processed_data: Dict[str, Dict]) -> None:
        try:
            for dataset_name, data in processed_data.items():
                fig = go.Figure(
                    data=[self.create_scatter_trace(
                        data[data.columns[0]],  # Date column
                        data['count'],
                        dataset_name
                    )]
                )
                
                fig.update_layout(
                    title=f"Data Analysis for {dataset_name}",
                    xaxis_title="Date",
                    yaxis_title="Count"
                )
                
                fig.show()
                
        except Exception as e:
            self.logger.error(f"Error creating plots: {str(e)}")
            raise