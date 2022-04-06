from abc import ABC, abstractmethod
from random import random

from pyautofinance.common.strategies.base_strategy import BaseStrategy


class ExitLimitedStrat(BaseStrategy):

    params = (
        ('stop_loss', 0),
        ('bars_in_market', 0),
        ('exit_proba', 0),
    )

    @abstractmethod
    def _open_short_condition(self) -> bool:
        pass

    @abstractmethod
    def _open_long_condition(self) -> bool:
        pass

    def _close_short_condition(self) -> bool:
        if self.p.bars_in_market:
            return len(self) - self.entry_bar >= self.p.bars_in_market
        if self.p.exit_proba:
            return random() < self.p.exit_proba
        return False

    def _close_long_condition(self) -> bool:
        if self.p.bars_in_market:
            return len(self) - self.entry_bar >= self.p.bars_in_market
        if self.p.exit_proba:
            return random() < self.p.exit_proba
        return False

    def _get_long_stop_loss_price(self):
        return self.datas[0].close[0] * (1 - self.params.stop_loss / 100) \
            if self.p.stop_loss else self.datas[0].close[0]

    def _get_short_stop_loss_price(self):
        return self.datas[0].close[0] * (1 + self.params.stop_loss / 100) \
            if self.p.stop_loss else self.datas[0].close[0]
