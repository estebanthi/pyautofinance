from enum import Enum
from dataclasses import dataclass, field
from pyautofinance.common.strategies._Strategy import _Strategy


class StrategyType(Enum):
    SIMPLE = 'SIMPLE'
    OPTIMIZED = 'OPTIMIZED'


@dataclass
class Strategy:
    strategy: _Strategy
    type: StrategyType
    parameters: dict = field(default_factory=dict)
    timeframes: list = field(default_factory=list)


class StrategiesFactory:

    def make_strategy(self, strategy, timeframes=[], **kwargs):
        strat_type = self._get_strategy_type(kwargs)
        return Strategy(strategy, strat_type, kwargs, timeframes)

    def _get_strategy_type(self, kwargs):
        strat_type = StrategyType.SIMPLE if not self._check_for_iterables_in_parameters(kwargs) else StrategyType.OPTIMIZED
        return strat_type

    @staticmethod
    def _check_for_iterables_in_parameters(kwargs):
        for v in kwargs.values():
            if hasattr(v, '__iter__') and type(v) != str:
                return True
