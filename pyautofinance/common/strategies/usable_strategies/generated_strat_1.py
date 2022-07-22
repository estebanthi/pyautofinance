from pyautofinance.common.strategies.base_strategy import BaseStrategy
from pyautofinance.common.strategies.generator.condition import Condition
import backtrader as bt
from backtrader.indicators.ema import ExponentialMovingAverage
from backtrader.indicators.bollinger import BollingerBands


class GeneratedStrategy1(BaseStrategy):

    def _init_indicators(self):
        self.rsi = bt.indicators.rsi.RelativeStrengthIndex(period=28)
        self.ema1 = ExponentialMovingAverage(period=59)
        self.bb1 = BollingerBands(period=44)
        self.ema2 = ExponentialMovingAverage(period=84)
        self.bb2 = BollingerBands(period=121)
        self.bb3 = BollingerBands(period=152)

    def _open_long_condition(self) -> bool:
        return self.rsi[0] < 100

    def _open_short_condition(self) -> bool:
        return self.ema1[0] <= self.datas[0].close[0]

    def _close_long_condition(self) -> bool:
        return self.bb1.bot[0] >= self.ema2[0]

    def _close_short_condition(self) -> bool:
        return self.bb2.bot[0] <= self.bb3.top[0]