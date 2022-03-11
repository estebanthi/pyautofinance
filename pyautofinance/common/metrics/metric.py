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
        analysis = self.get_analysis_from_strat(strat)
        self.value = self.get_metric_from_analysis(analysis)

    def __repr__(self):
        return self.name + ' : ' + str(self.value)

    def get_analysis_from_strat(self, strat):
        try:
            analyzer = getattr(strat.analyzers, self.analyzer_name)
        except AttributeError:
            raise AnalyzerMissing(self.analyzer_name)

        return analyzer.get_analysis()

    @abstractmethod
    def get_metric_from_analysis(self, strat):
        pass

    @abstractmethod
    def __gt__(self, other):
        pass
