from abc import ABC, abstractmethod

from pyautofinance.common.strategies.test_strats.monkey_strat import MonkeyStrat


class EntryMonkeyStrat(MonkeyStrat, ABC):

    @abstractmethod
    def _close_short_condition(self) -> bool:
        pass

    @abstractmethod
    def _close_long_condition(self) -> bool:
        pass
