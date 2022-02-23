from dataclasses import dataclass
import backtrader as bt
from dataclasses import field
from pyautofinance.common.analyzers.CustomReturns import CustomReturns
from backtrader.analyzers.drawdown import DrawDown


class CalmarRatio(bt.Analyzer):

    def __init__(self):
        self.cr = CustomReturns()
        self.dd = DrawDown()


    def get_analysis(self):
        ann_ret = self.cr.get_analysis()["ann_ret"]
        max_dd = self.dd.get_analysis().max.drawdown
        return {"calmar_ratio": ann_ret/max_dd}

