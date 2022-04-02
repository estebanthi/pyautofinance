from abc import abstractmethod

from pyautofinance.common.metrics.metric import Metric


class LearnMetric(Metric):

    def __init__(self, y_true, y_pred):
        self.y_true = y_true
        self.y_pred = y_pred
        super().__init__()

    @abstractmethod
    def _get_metric_value(self):
        pass

    @abstractmethod
    def __gt__(self, other):
        pass