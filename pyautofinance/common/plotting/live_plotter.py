from btplotting import BacktraderPlottingLive
from btplotting.schemes import Blackly

from pyautofinance.common.engine.engine_component import EngineComponent
from pyautofinance.common.config.config import Config


class LivePlotter(EngineComponent):

    def __init__(self, scheme=Blackly()):
        self.scheme = scheme

    def attach_to_engine(self, engine):
        config = Config()
        engine.cerebro.addanalyzer(BacktraderPlottingLive, port=config['live_app_port'], scheme=self.scheme)
