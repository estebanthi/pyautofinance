import backtrader as bt
import math
import statistics


class ReturnsVolatility(bt.Analyzer):

    def __init__(self):
        self.returns = []

    def notify_trade(self, trade):
        if trade.isclosed:
            brokervalue = self.strategy.broker.getvalue()

            pnl = trade.history[len(trade.history) - 1].status.pnlcomm
            pnl_percent = 100 * pnl / brokervalue

            self.returns.append(pnl_percent)

    def get_analysis(self):
        return {"volatility": math.sqrt(statistics.variance(self.returns))}
