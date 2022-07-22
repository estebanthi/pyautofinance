import backtrader as bt
from backtrader.indicators.rsi import RelativeStrengthIndex

from pyautofinance.common.strategies.generator.line import Line
from pyautofinance.common.strategies.generator.types import Type
from pyautofinance.common.strategies.generator.param import Param


class RSILine(Line):
    parent = RelativeStrengthIndex
    mapping = 'rsi'
    type = Type.RANGE_COMPARABLE
    comparisons_available = ['>', '<', '>=', '<=', '==', '!=']
    range = (0, 100)

    def __init__(self):
        super().__init__([Param('period', range(3, 50))])
