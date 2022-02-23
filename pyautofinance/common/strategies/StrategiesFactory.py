from enum import Enum
from collections import namedtuple


Strategy = namedtuple('Strategy', ['classname', 'parameters', 'type'])


class StrategiesFactory:

    def make_strategy(self, strategy, **kwargs):
        strat_type = self._get_strategy_type(kwargs)
        return Strategy(strategy, kwargs, strat_type)

    def _get_strategy_type(self, kwargs):
        strat_type = StrategyType.SIMPLE if not self._check_for_iterables_in_parameters(kwargs) else StrategyType.OPTIMIZED
        return strat_type

    @staticmethod
    def _check_for_iterables_in_parameters(kwargs):
        for v in kwargs.values():
            if hasattr(v, '__iter__') and type(v) != str:
                return True


class StrategyType(Enum):
    SIMPLE = 'SIMPLE'
    OPTIMIZED = 'OPTIMIZED'
