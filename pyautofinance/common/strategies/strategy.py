from pyautofinance.common.engine.engine_component import EngineComponent


class Strategy(EngineComponent):

    def __init__(self, bt_strat, name='', **parameters):
        self._bt_strat = bt_strat
        self._parameters = parameters
        self.timeframes = parameters.get('timeframes', list())
        self.name = name

    def attach_to_engine(self, engine):
        engine.cerebro.optstrategy(self._bt_strat, **self._parameters)
        engine.cerebro.strategy_name = self.name

    def set_parameters(self, parameters):
        self._parameters = parameters

    def get_parameters(self):
        return self._parameters
