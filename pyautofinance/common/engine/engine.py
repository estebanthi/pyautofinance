import backtrader as bt

from pyautofinance.common.engine.engine_cerebro import EngineCerebro
from pyautofinance.common.results.engine_result import EngineResult
from pyautofinance.common.analyzers import TradeList


class Engine:

    def __init__(self, components_assembly):
        self._components_assembly = components_assembly
        self.cerebro = EngineCerebro()

    def _build(self):
        for component in self._components_assembly:
            component.attach_to_engine(self)
        self.cerebro.addanalyzer(TradeList, _name='tradelist')

    def run(self):
        self.cerebro = EngineCerebro()
        self._build()

        cerebro_result = self.cerebro.run(optreturn=True, tradehistory=True, maxcpus=1)
        return EngineResult(cerebro_result, self._components_assembly[4])

    def plot(self, scheme={"style": 'candlestick', "barup": "green"}):
        self.cerebro.plot(**scheme)

    def get_timeframes(self):
        return self._components_assembly[1].timeframes
