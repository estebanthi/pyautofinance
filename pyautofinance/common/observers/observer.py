from pyautofinance.common.engine.engine_component import EngineComponent


class Observer(EngineComponent):

    def __init__(self, bt_observer, **parameters):
        self._bt_observer = bt_observer
        self._parameters = parameters

    def attach_to_engine(self, engine):
        engine.cerebro.addobserver(self._bt_observer, **self._parameters)