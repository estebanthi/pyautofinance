import backtrader as bt


class Candle(bt.Indicator):

    lines = ('open', 'high', 'low', 'close')

    def next(self):
        self.lines.open[0] = self.datas[0].open[0]
        self.lines.high[0] = self.datas[0].high[0]
        self.lines.low[0] = self.datas[0].low[0]
        self.lines.close[0] = self.datas[0].close[0]
