import backtrader as bt
import statistics


class TradesAverageReturns(bt.Analyzer):

    def __init__(self):
        self.returns = []

    def notify_trade(self, trade):
        if trade.isclosed:
            trade_side = self._get_trade_side(trade)
            brokervalue = self.strategy.broker.getvalue()

            pnl = trade.history[len(trade.history) - 1].status.pnlcomm
            pnl_percent = 100 * pnl / brokervalue

            self.returns.append([pnl_percent, trade_side])

    @staticmethod
    def _get_trade_side(trade):
        trade_side = 'short'
        if trade.history[0].event.size > 0:
            trade_side = 'long'
        return trade_side

    def get_analysis(self):
        return {
            "average_returns": statistics.mean([item[0] for item in self.returns]),
            "average_returns_short": statistics.mean([item[0] for item in self.returns if item[1] == "short"]),
            "average_returns_long": statistics.mean([item[0] for item in self.returns if item[1] == "long"])
        }
