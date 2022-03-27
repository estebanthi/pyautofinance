import pandas as pd

from pyautofinance.common.metrics.metric import Metric


class AverageReturns(Metric):
    name = 'AverageReturns'
    monte_carlo_results_dataframe: pd.DataFrame

    def __init__(self, monte_carlo_results_dataframe):
        self.monte_carlo_results_dataframe = monte_carlo_results_dataframe
        super().__init__()

    def _get_metric_value(self):
        return self.monte_carlo_results_dataframe['returns'].mean()

    def __gt__(self, other):
        return self.value > other.value
