import backtrader as bt

from pyautofinance.common.strategies.generator.line import Line
from pyautofinance.common.strategies.generator.types import Type
from pyautofinance.common.strategies.generator.param import Param

from backtrader.indicators.bollinger import BollingerBands


class BollingerBotBandLine(Line):
    parent = BollingerBands
    mapping = 'bot'
    type = Type.PRICE_COMPARABLE
    comparisons_available = ['>', '<', '>=', '<=', '==', '!=']

    def __init__(self):
        super().__init__([Param('period', range(3, 200))])
