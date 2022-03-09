from pyautofinance.common.engine.engine_component import EngineComponent


class Sizer(EngineComponent):

    def __init__(self, bt_sizer, **parameters):
        self._bt_sizer = bt_sizer
        self._parameters = parameters

    def attach_to_engine(self, engine):
        engine.cerebro.addsizer(self._bt_sizer, **self._parameters)
