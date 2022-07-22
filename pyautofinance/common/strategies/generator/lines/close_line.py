import backtrader as bt

from pyautofinance.common.strategies.generator.line import Line
from pyautofinance.common.strategies.generator.types import Type
from pyautofinance.common.indicators.candle import Candle


class CloseLine(Line):
    parent = Candle
    mapping = 'close'
    type = Type.PRICE_COMPARABLE
    comparisons_available = ['>', '<', '>=', '<=', '==', '!=']
