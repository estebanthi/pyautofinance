from pyautofinance.common.engine.engine_component import EngineComponent
from abc import abstractmethod


class Datafeed(EngineComponent):

    @abstractmethod
    def __init__(self, symbol, start_date, timeframe):
        self._symbol = symbol
        self._start_date = start_date
        self._timeframe = timeframe
        self._bt_datafeed = None

    def attach_to_engine(self, engine):
        engine.cerebro.adddata(self._bt_datafeed)
        self._attach_resampled_datafeed_to_engine(self._bt_datafeed, engine)

    @staticmethod
    def _attach_resampled_datafeed_to_engine(bt_datafeed, engine):
        timeframes = engine.get_timeframes()
        for timeframe in timeframes:
            engine.cerebro.resampledata(bt_datafeed, timeframe=timeframe.bt_timeframe,
                                        compression=timeframe.bt_compression)
