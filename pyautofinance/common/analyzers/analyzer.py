from pyautofinance.common.engine.engine_component import EngineComponent


class Analyzer(EngineComponent):

    def __init__(self, bt_analyzer, name, **parameters):
        self._bt_analyzer = bt_analyzer
        self._name = name
        self._parameters = parameters

    def attach_to_engine(self, engine):
        engine.cerebro.addanalyzer(self._bt_analyzer, _name=self._name, **self._parameters)
