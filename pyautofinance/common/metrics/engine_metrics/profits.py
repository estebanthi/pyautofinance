from pyautofinance.common.metrics.engine_metrics.engine_metric import EngineMetric
from pyautofinance.common.analyzers import TradeAnalyzer


class TotalGrossProfit(EngineMetric):

    name = 'TotalGrossProfit'
    analyzers = [TradeAnalyzer()]

    def _get_metric_from_analysis(self, analysis):
        return analysis[0].pnl.gross.total

    def __gt__(self, other):
        return self.value > other.value


class TotalNetProfit(EngineMetric):

    name = 'TotalNetProfit'
    analyzers = [TradeAnalyzer()]

    def _get_metric_from_analysis(self, analysis):
        return analysis[0].pnl.net.total

    def __gt__(self, other):
        return self.value > other.value
