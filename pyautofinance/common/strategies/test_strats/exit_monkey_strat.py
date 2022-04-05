from abc import ABC, abstractmethod

from pyautofinance.common.strategies.test_strats.monkey_strat import MonkeyStrat


class ExitMonkeyStrat(MonkeyStrat, ABC):

    @abstractmethod
    def _open_short_condition(self) -> bool:
        pass

    @abstractmethod
    def _open_long_condition(self) -> bool:
        pass
