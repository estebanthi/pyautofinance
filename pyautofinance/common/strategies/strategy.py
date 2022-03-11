from pyautofinance.common.engine.engine_component import EngineComponent


class Strategy(EngineComponent):

    def __init__(self, bt_strat, **parameters):
        self._bt_strat = bt_strat
        self._parameters = parameters

    def attach_to_engine(self, engine):
        engine.optstrategy(self._bt_strat, **self._parameters)
