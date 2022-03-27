from abc import abstractmethod
from dataclasses import dataclass

from pyautofinance.common.analyzers.analyzer import Analyzer
from pyautofinance.common.exceptions.analyzers import AnalyzerMissing

from pyautofinance.common.metrics.metric import Metric


@dataclass
class EngineMetric(Metric):
    analyzer: Analyzer

    def __init__(self, strat):
        self._strat = strat
        self.value = self._get_metric_value()

    def _get_analysis(self):
        try:
            analyzer = getattr(self._strat.analyzers, self.analyzer.name)
        except AttributeError:
            raise AnalyzerMissing(self.analyzer.name)

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
