from math import sqrt

import backtrader as bt


class AverageGainPerTrade(bt.Observer):

    lines = ('average', 'real', 'up', 'down')

    params = (
        ('average_gain', 100),
        ('standard_deviation', 30),
        ('X', 1),
    )

    plotinfo = dict(plot=True, subplot=True, plotlinelabels=True)

    plotlines = dict(
        average=dict(color='blue'),
        real=dict(color='magenta'),
        down=dict(color='yellow'),
        up=dict(color='yellow'),
    )

    def next(self):
        n = len(self)
        average_gain = self.p.average_gain
        std_dev = self.p.standard_deviation
        X = self.p.X

        self.lines.average[0] = n * average_gain
        self.lines.real[0] = self._owner.stats.broker.value[0] - self._owner.initial_cash
        self.lines.up[0] = n * average_gain + sqrt(n) * std_dev * X
        self.lines.down[0] = n * average_gain - sqrt(n) * std_dev * X
