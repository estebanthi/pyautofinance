from backtrader_plotting.schemes import Blackly
from backtrader_plotting import Bokeh

from pyautofinance.common.engine.engine_component import EngineComponent


class BackPlotter(EngineComponent):

    def __init__(self, scheme=Blackly(), **params):
        self.bokeh = Bokeh(scheme=scheme, **params)

    def attach_to_engine(self, engine):
        engine.cerebro.bokeh = self.bokeh
