from pyautofinance.common.engine.engine_component import EngineComponent


class Strategy(EngineComponent):

    def __init__(self, bt_strat, **parameters):
        self._bt_strat = bt_strat
        self._parameters = parameters
        self.timeframes = parameters.get('timeframes', list())

    def attach_to_engine(self, engine):
        engine.cerebro.optstrategy(self._bt_strat, **self._parameters)
