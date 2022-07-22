import backtrader as bt


class Value(bt.Indicator):

    lines = ('value',)
    params = (('value', 0),)

    def next(self):
        self.lines.value[0] = self.params.value
