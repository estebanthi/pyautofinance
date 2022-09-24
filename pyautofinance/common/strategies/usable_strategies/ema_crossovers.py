from backtrader.indicators import ExponentialMovingAverage as EMA

from pyautofinance.common.strategies.bracket_strategy import BracketStrategy


class EMACrossOvers(BracketStrategy):

    params = (
        ('ema_period', 200),
    )

    def _init_indicators(self):
        self.ema = EMA(period=self.p.ema_period)

    def _open_long_condition(self) -> bool:
        if self.ema[0] > self.datas[0].close[0]:
            return False

    def _open_short_condition(self) -> bool:
        if self.ema[0] < self.datas[0].close[0]:
            return True
