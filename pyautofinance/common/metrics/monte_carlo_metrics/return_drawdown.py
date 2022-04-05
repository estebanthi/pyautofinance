import numpy as np

from pyautofinance.common.metrics.metric import Metric


class ReturnDrawdown(Metric):
    name = 'ReturnDrawdown'

    def __init__(self, returns, drawdown):
        self.returns = returns
        self.drawdown = drawdown
        super().__init__()

    def _get_metric_value(self):
        return self.returns / self.drawdown

    def __gt__(self, other):
        return self.value > other.value
