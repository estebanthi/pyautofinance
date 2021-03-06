import numpy as np

from pyautofinance.common.metrics.metric import Metric


class RiskOfRuin(Metric):
    name = 'RiskOfRuin'

    def __init__(self, ruined_list):
        self.ruined_list = ruined_list
        super().__init__()

    def _get_metric_value(self):
        array = np.array(self.ruined_list)
        return 1 - array.mean()

    def __gt__(self, other):
        return self.value < other.value
