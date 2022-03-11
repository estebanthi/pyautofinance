from abc import ABC, abstractmethod
from dataclasses import dataclass

import backtrader as bt

from pyautofinance.common.exceptions.analyzers import AnalyzerMissing


@dataclass
class Metric(ABC):
    name: str
    analyzer_name: str
    bt_analyzer: bt.Analyzer
    value: any = 0

    def __init__(self, strat):
        self._strat = strat
        self.value = self._get_metric_value()

    def __repr__(self):
        return self.name + ' : ' + str(self.value)

    def _get_analysis(self):
        try:
            analyzer = getattr(self._strat.analyzers, self.analyzer_name)
        except AttributeError:
            raise AnalyzerMissing(self.analyzer_name)

        return analyzer.get_analysis()

    @abstractmethod
    def _get_metric_from_analysis(self, analysis):
        pass

    def _get_metric_value(self):
        analysis = self._get_analysis()
        return self._get_metric_from_analysis(analysis)

    @abstractmethod
    def __gt__(self, other):
        pass
