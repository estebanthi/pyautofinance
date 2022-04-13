from math import sqrt

from pyautofinance.common.metrics.engine_metrics.engine_metric import EngineMetric
from pyautofinance.common.analyzers.trade_analyzer import TradeAnalyzer
from pyautofinance.common.analyzers.trade_list import TradeList


class StandardDeviation(EngineMetric):

    name = 'StandardDeviation'
    analyzers = [TradeAnalyzer(), TradeList()]

    def _get_metric_from_analysis(self, analysis):
        trade_analyzer_analysis = analysis[0]
        trade_list_analysis = analysis[1]

        n = trade_analyzer_analysis.total.total
        average = trade_analyzer_analysis.pnl.net.average
        trades_pnls = [trade['pnl'] for trade in trade_list_analysis['trades']]

        std_dev = sqrt(
            sum([(pnl - average)**2 for pnl in trades_pnls]) / n
        )

        return std_dev

    def __gt__(self, other):
        return self.value < other.value
