from backtrader_plotting import OptBrowser

from pyautofinance.common.engine.engine_cerebro import EngineCerebro
from pyautofinance.common.results.engine_result import EngineResult
from pyautofinance.common.analyzers import TradeList


class Engine:

    def __init__(self, components_assembly, optimized=True):
        self.components_assembly = components_assembly
        self.optimized = optimized
        self.cerebro = EngineCerebro()

    def _build(self):
        for component in self.components_assembly:
            component.attach_to_engine(self)
        TradeList().attach_to_engine(self)

    def run(self):
        self.cerebro = EngineCerebro()
        self._build()
        cerebro_result = self.cerebro.run(optreturn=self.optimized, tradehistory=True, maxcpus=1)
        result = self._get_result(cerebro_result)
        self._plot(cerebro_result)
        return result

    def _get_result(self, cerebro_result):
        return EngineResult(cerebro_result, self.components_assembly[4], self.components_assembly[2])

    def plot(self, bokeh):
        self.cerebro.plot(bokeh)

    def _plot(self, cerebro_result):
        if hasattr(self.cerebro, 'opt_plotting'):
            browser = OptBrowser(self.cerebro.bokeh, cerebro_result)
            browser.start()
        elif hasattr(self.cerebro, 'bokeh'):
            self.plot(self.cerebro.bokeh)

    def get_timeframes(self):
        return self.components_assembly[1].timeframes

    def add_dataflux(self, dataflux):
        self._get_result = self.write_result(self._get_result, dataflux)
        self.cerebro.dataflux = dataflux

    def write_result(self, get_result, dataflux):
        def wrapper():
            result = get_result()
            dataflux.write(result)
            return result
        return wrapper
