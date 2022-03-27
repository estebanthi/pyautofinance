import pandas as pd

from pyautofinance.common.metrics.metric import Metric


class AverageMaxDrawdown(Metric):
    name = 'AverageMaxDrawdown'
    monte_carlo_results_dataframe: pd.DataFrame

    def __init__(self, monte_carlo_results_dataframe):
        self.monte_carlo_results_dataframe = monte_carlo_results_dataframe
        super().__init__()

    def _get_metric_value(self):
        return self.monte_carlo_results_dataframe['max_drawdown'].mean()

    def __gt__(self, other):
        return self.value < other.value
