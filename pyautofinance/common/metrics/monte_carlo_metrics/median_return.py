import numpy as np

from pyautofinance.common.metrics.metric import Metric


class MedianReturn(Metric):
    name = 'MedianReturn'

    def __init__(self, returns):
        self.returns = returns
        super().__init__()

    def _get_metric_value(self):
        array = np.array(self.returns)
        return np.median(array)

    def __gt__(self, other):
        return self.value > other.value
