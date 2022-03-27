from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Metric(ABC):
    name: str
    value: any

    def __init__(self):
        self.value = self._get_metric_value()

    def __repr__(self):
        return self.name + ' : ' + str(self.value)

    @abstractmethod
    def _get_metric_value(self):
        pass

    @abstractmethod
    def __gt__(self, other):
        pass
