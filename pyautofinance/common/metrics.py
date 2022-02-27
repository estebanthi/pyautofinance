from abc import ABC, abstractmethod
from dataclasses import dataclass
import backtrader as bt

from pyautofinance.common.exceptions.analyzers import AnalyzerMissing


@dataclass
class Metric(ABC):
    name: str
    analyzer_to_get_metric_from: bt.Analyzer
    value: any = 0

    def __init__(self, strat):
        analysis = self.get_analysis_from_strat(strat)
        self.value = self.get_metric_from_analysis(analysis)

    def __repr__(self):
        return self.name + ' : ' + str(self.value)

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
    def __gt__(self, other):
        pass


class TotalGrossProfit(Metric):

    name = 'TotalGrossProfit'
    analyzer_to_get_metric_from = bt.analyzers.TradeAnalyzer

    def get_metric_from_analysis(self, analysis):
        return analysis.pnl.gross.total

    def __gt__(self, other):
        return self.value > other.value
