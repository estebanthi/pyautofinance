import pandas as pd

from pyautofinance.common.metrics.metric import Metric
from pyautofinance.common.metrics.miscellaneous_metrics.average_returns import AverageReturns
from pyautofinance.common.metrics.miscellaneous_metrics.average_max_drawdown import AverageMaxDrawdown


class AverageReturnsDrawdown(Metric):
    name = 'AverageReturnsDrawdown'
    monte_carlo_results_dataframe: pd.DataFrame

    def __init__(self, monte_carlo_results_dataframe):
        self.monte_carlo_results_dataframe = monte_carlo_results_dataframe
        super().__init__()

    def _get_metric_value(self):
        average_max_drawdown = AverageMaxDrawdown(self.monte_carlo_results_dataframe).value
        average_returns = AverageReturns(self.monte_carlo_results_dataframe).value
        return average_returns / average_max_drawdown

    def __gt__(self, other):
        return self.value > other.value
