import numpy as np

from pyautofinance.common.metrics.metric import Metric


class MedianProfit(Metric):
    name = 'MedianProfit'

    def __init__(self, profits):
        self.profits = profits
        super().__init__()

    def _get_metric_value(self):
        array = np.array(self.profits)
        return np.median(array)

    def __gt__(self, other):
        return self.value > other.value
