import backtrader as bt

from pyautofinance.common.metrics.metric import Metric


class TotalGrossProfit(Metric):

    name = 'TotalGrossProfit'
    analyzer_name = 'tradeanalyzer'
    bt_analyzer = bt.analyzers.TradeAnalyzer

    def get_metric_from_analysis(self, analysis):
        return analysis.pnl.gross.total

    def __gt__(self, other):
        return self.value > other.value
