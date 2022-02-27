from abc import ABC, abstractmethod
from dataclasses import dataclass
import backtrader as bt

from pyautofinance.common.exceptions.analyzers import AnalyzerMissing


class MetricsCollection:

    def __init__(self, metrics_list):
        self.metrics_list = metrics_list

    def __getitem__(self, item):
        return self.metrics_list[item]

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.metrics_list):
            metric = self.metrics_list[self.index]
            self.index += 1
            return metric
        else:
            raise StopIteration


@dataclass
class Metric(ABC):
    name: str
    analyzer_to_get_metric_from: bt.Analyzer
    value: any = 0

    def __init__(self, strat):
        analysis = self.get_analysis_from_strat(strat)
        self.value = self.get_metric_from_analysis(analysis)

    def get_analysis_from_strat(self, strat):

        class AnalysisFactory:

            @staticmethod
            def get_analysis(analyzer):
                analysis = None
                if analyzer == bt.analyzers.TradeAnalyzer:
                    try:
                        analysis = strat.analyzers.tradeanalyzer.get_analysis()
                    except AttributeError:
                        raise AnalyzerMissing('Trade Analyzer')
                return analysis

        return AnalysisFactory.get_analysis(self.analyzer_to_get_metric_from)

    @abstractmethod
    def get_metric_from_analysis(self, strat):
        pass

    @abstractmethod
    def is_better_than_other(self, other) -> bool:
        pass


class TotalGrossProfit(Metric):

    name = 'TotalGrossProfit'
    analyzer_to_get_metric_from = bt.analyzers.TradeAnalyzer

    def get_metric_from_analysis(self, analysis):
        return analysis.pnl.gross.total

    def is_better_than_other(self, other):
        return self.value > other
