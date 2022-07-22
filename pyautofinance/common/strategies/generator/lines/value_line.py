import backtrader as bt

from pyautofinance.common.strategies.generator.line import Line
from pyautofinance.common.strategies.generator.types import Type
from pyautofinance.common.strategies.generator.param import Param
from pyautofinance.common.indicators.value import Value


class ValueLine(Line):
    parent = Value
    mapping = 'value'
    type = Type.NOT_COMPARABLE
    comparisons_available = ['>', '<', '>=', '<=', '==', '!=']

    def __init__(self, possible_values):
        super().__init__([Param('value', possible_values)])
