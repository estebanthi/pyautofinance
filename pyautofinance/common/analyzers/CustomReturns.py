import backtrader as bt
import math


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
