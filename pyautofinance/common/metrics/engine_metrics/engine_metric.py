from abc import abstractmethod
from dataclasses import dataclass

from pyautofinance.common.analyzers.analyzer import Analyzer
from pyautofinance.common.exceptions.analyzers import AnalyzerMissing

from pyautofinance.common.metrics.metric import Metric


@dataclass
class EngineMetric(Metric):
    analyzers: list

    def __init__(self, strat):
        self._strat = strat
        self.value = self._get_metric_value()

    def _get_analysis(self):
        analysis = []
        for analyzer in self.analyzers:
            analysis.append(self._get_analysis_for_one(analyzer))

        return analysis

    def _get_analysis_for_one(self, analyzer):
        try:
            analyzer = getattr(self._strat.analyzers, analyzer.name)
        except AttributeError:
            raise AnalyzerMissing(analyzer.name)

        return analyzer.get_analysis()

    @abstractmethod
    def _get_metric_from_analysis(self, analysis):
        pass

    def _get_metric_value(self):
        analysis = self._get_analysis()
        metric = 0

        try:
            metric = self._get_metric_from_analysis(analysis)
        except KeyError as e:
            pass

        return metric

    @abstractmethod
    def __gt__(self, other):
        pass

    def __repr__(self):
        return self.name + ' : ' + str(self.value)