from random import random

from pyautofinance.common.strategies.base_strategy import BaseStrategy


class MonkeyStrat(BaseStrategy):

    params = (
        ('entries_proba', 0.5),
        ('exits_proba', 0.5)
    )

    def _open_short_condition(self) -> bool:
        return random() < self.p.entries_proba

    def _open_long_condition(self) -> bool:
        return random() < self.p.entries_proba

    def _close_short_condition(self) -> bool:
        return random() < self.p.exits_proba

    def _close_long_condition(self) -> bool:
        return random() < self.p.exits_proba
