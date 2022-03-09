from pyautofinance.common.engine.engine_component import EngineComponent


class Analyzer(EngineComponent):

    def __init__(self, bt_analyzer, **parameters):
        self._bt_analyzer = bt_analyzer
        self._parameters = parameters

    def attach_to_engine(self, engine):
        engine.cerebro.addanalyzer(self._bt_analyzer, **self._parameters)