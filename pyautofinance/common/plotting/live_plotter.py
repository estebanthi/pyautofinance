from btplotting import BacktraderPlottingLive
from btplotting.schemes import Blackly

from pyautofinance.common.engine.engine_component import EngineComponent


class LivePlotter(EngineComponent):

    def __init__(self, scheme=Blackly()):
        self.scheme = scheme

    def attach_to_engine(self, engine):
        engine.cerebro.addanalyzer(BacktraderPlottingLive, scheme=self.scheme)
