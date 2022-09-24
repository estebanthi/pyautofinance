import backtrader as bt


class GuppyMultipleMovingAverages(bt.Indicator):

    lines = ('short', 'medium', 'long', 'extreme')
    plotlines = dict(short=dict(color='red'), medium=dict(color='green'), long=dict(color='blue'), extreme=dict(color='orange'))
    plotinfo = dict(subplot=False, plotlinelabels=True, plot=True, plotname='GMMA', plotyhlines=[0], plotyticks=[0])

    params = (
        ('short', 5),
        ('medium', 8),
        ('long', 13),
        ('extreme', 21)
    )

    def __init__(self):
        self.short = bt.ind.EMA(period=self.p.short)
        self.medium = bt.ind.EMA(period=self.p.medium)
        self.long = bt.ind.EMA(period=self.p.long)
        self.extreme = bt.ind.EMA(period=self.p.extreme)

    def next(self):
        self.lines.short[0] = self.short[0]
        self.lines.medium[0] = self.medium[0]
        self.lines.long[0] = self.long[0]
        self.lines.extreme[0] = self.extreme[0]

    def _plotlabel(self):
        return ['GMMA']
