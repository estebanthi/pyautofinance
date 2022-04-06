from abc import ABC, abstractmethod
from random import random

from pyautofinance.common.strategies.base_strategy import BaseStrategy


class EntryLimitedStrat(BaseStrategy):

    params = (
        ('bars_in_market', 0),
        ('entry_proba', 0),
    )

    @abstractmethod
    def _close_short_condition(self) -> bool:
        pass

    @abstractmethod
    def _close_long_condition(self) -> bool:
        pass

    def _open_short_condition(self) -> bool:
        if self.p.bars_in_market:
            return len(self) % self.p.bars_in_market == 0
        if self.p.entry_proba:
            return random() < self.p.entry_proba

    def _open_long_condition(self) -> bool:
        if self.p.bars_in_market:
            return len(self) % self.p.bars_in_market == 0
        if self.p.entry_proba:
            return random() < self.p.entry_proba

