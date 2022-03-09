import backtrader as bt
import math
import statistics


class CustomReturns(bt.TimeFrameAnalyzerBase):
    minutes_in_a_day = 1440

    timeframes_mapper = {
        bt.TimeFrame.Minutes: 1,
        bt.TimeFrame.Days: minutes_in_a_day
    }

    def __init__(self):
        self._value_start = self.strategy.broker.getvalue()
        self._value_end = 0
        self._total_returns = 0
        self._average_returns = 0
        self._annual_returns = 0
        self._log_returns = 0
        self._bar_count = 0

    def stop(self):
        self._value_end = self.strategy.broker.getvalue()

        self._total_returns = (self._value_end / self._value_start - 1) * 100
        self._average_returns = self._total_returns / self._bar_count

        self._annual_returns = 525_600 / (self.timeframes_mapper[self.timeframe] * self.compression) \
                               * self._average_returns

        self._log_returns = math.log(abs(self._annual_returns) / 100) * 100

    def get_analysis(self):

        return {
            "total_returns": self._total_returns,
            "annual_returns": self._annual_returns,
            "log_returns": self._log_returns
        }

    def _on_dt_over(self):
        self._bar_count += 1  # Counter incrementing for each iteration in the backtest


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
