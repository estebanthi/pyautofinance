import numpy as np

from pyautofinance.common.metrics.metric import Metric


class MaxDrawdownFromEquity(Metric):
    name = 'MaxDrawdownFromEquity'
    equities: list

    def __init__(self, equities):
        self.equities = equities
        super().__init__()

    def _get_metric_value(self):
        drawdown_low_index = np.argmax(np.maximum.accumulate(self.equities) - self.equities)  # end of the period
        drawdown_peak_index = np.argmax(self.equities[:drawdown_low_index])

        low = self.equities[drawdown_low_index]
        peak = self.equities[drawdown_peak_index]

        drawdown = (peak - low) / peak
        return drawdown

    def __gt__(self, other):
        return self.value < other.value
