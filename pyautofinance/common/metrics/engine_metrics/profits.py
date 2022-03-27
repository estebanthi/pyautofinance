from pyautofinance.common.metrics.engine_metric import EngineMetric
from pyautofinance.common.analyzers import TradeAnalyzer


class TotalGrossProfit(EngineMetric):

    name = 'TotalGrossProfit'
    analyzer = TradeAnalyzer()

    def _get_metric_from_analysis(self, analysis):
        return analysis.pnl.gross.total

    def __gt__(self, other):
        return self.value > other.value


class TotalNetProfit(EngineMetric):

    name = 'TotalNetProfit'
    analyzer = TradeAnalyzer()

    def _get_metric_from_analysis(self, analysis):
        return analysis.pnl.net.total

    def __gt__(self, other):
        return self.value > other.value
