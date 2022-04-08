from abc import abstractmethod
from dataclasses import dataclass

from pyautofinance.common.metrics.metric import Metric


@dataclass
class LiveMetric(Metric):

    name: str

    def __init__(self):
        self.value = 0

    def _get_metric_value(self):
        return self._get_metric_from_strat(self._strat)

    @abstractmethod
    def _get_value_from_strat(self, strat):
        pass

    @abstractmethod
    def __gt__(self, other):
        pass

    def update(self, strat):
        self.value = self._get_value_from_strat(strat)
