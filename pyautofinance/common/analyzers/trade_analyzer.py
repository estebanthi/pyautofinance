import backtrader as bt

from pyautofinance.common.analyzers.analyzer import Analyzer


class TradeAnalyzer(Analyzer):

    def __init__(self):
        super().__init__('tradeanalyzer')

    def get_bt_analyzer(self) -> bt.Analyzer:
        return bt.analyzers.TradeAnalyzer
