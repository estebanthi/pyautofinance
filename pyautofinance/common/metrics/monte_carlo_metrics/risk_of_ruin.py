import pandas as pd

from pyautofinance.common.metrics.metric import Metric


class RiskOfRuin(Metric):
    name = 'RiskOfRuin'
    monte_carlo_results_dataframe: pd.DataFrame

    def __init__(self, monte_carlo_results_dataframe):
        self.monte_carlo_results_dataframe = monte_carlo_results_dataframe
        super().__init__()

    def _get_metric_value(self):
        ruined = self.monte_carlo_results_dataframe['ruined'][self.monte_carlo_results_dataframe['ruined'] == True]
        return len(ruined) / len(self.monte_carlo_results_dataframe)

    def __gt__(self, other):
        return self.value < other.value if isinstance(other, Metric) else self.value < other
