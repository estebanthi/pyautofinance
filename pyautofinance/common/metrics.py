from abc import ABC, abstractmethod
from dataclasses import dataclass
import backtrader as bt


class MetricsCollection:

    def __init__(self, metrics_list):
        self.metrics_list = metrics_list

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

    def __init__(self, name, analyzer_to_get_metric_from):
        self.name = name
        self.analyzer_to_get_metric_from = analyzer_to_get_metric_from

    def set_value_from_strat(self, strat):
        self.value = self.get_metric_from_strat(strat)

    @abstractmethod
    def get_metric_from_strat(self, strat):
        pass


class TotalGrossProfit(Metric):

    def __init__(self):
        super().__init__('TotalGrossProfit', bt.analyzers.TradeAnalyzer)

    @staticmethod
    def get_metric_from_strat(strat):
        tradeanalyzer = strat.analyzers.tradeanalyzer
        analysis = tradeanalyzer.get_analysis()
        return analysis.pnl.gross.total


