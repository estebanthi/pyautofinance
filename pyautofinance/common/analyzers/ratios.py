import backtrader as bt

from backtrader.analyzers import DrawDown

from pyautofinance.common.analyzers import CustomReturns


class CalmarRatio(bt.Analyzer):

    def __init__(self):
        self.custom_returns = CustomReturns()
        self.draw_down = DrawDown()

    def get_analysis(self):
        ann_ret = self.custom_returns.get_analysis()["annual_returns"]
        max_dd = self.draw_down.get_analysis().max.drawdown
        return {"calmar_ratio": ann_ret/max_dd}
