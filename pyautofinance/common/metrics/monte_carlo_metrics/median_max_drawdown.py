import numpy as np

from pyautofinance.common.metrics.metric import Metric


class MedianMaxDrawdown(Metric):
    name = 'MedianMaxDrawdown'

    def __init__(self, drawdowns):
        self.drawdowns = drawdowns
        super().__init__()

    def _get_metric_value(self):
        array = np.array(self.drawdowns)
        return np.median(array)

    def __gt__(self, other):
        return self.value < other.value
