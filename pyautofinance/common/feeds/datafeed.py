from abc import abstractmethod

import backtrader as bt

from pyautofinance.common.engine.engine_component import EngineComponent


class Datafeed(EngineComponent):

    @abstractmethod
    def __init__(self, symbol, start_date, timeframe):
        self._symbol = symbol
        self._start_date = start_date
        self._timeframe = timeframe

    @abstractmethod
    def _get_bt_datafeed(self) -> bt.DataBase:
        pass

    def attach_to_engine(self, engine):
        bt_datafeed = self._get_bt_datafeed()
        engine.cerebro.adddata(bt_datafeed)
        self._attach_resampled_datafeed_to_engine(bt_datafeed, engine)

    @staticmethod
    def _attach_resampled_datafeed_to_engine(bt_datafeed, engine):
        timeframes = engine.get_timeframes()
        for timeframe in timeframes:
            engine.cerebro.resampledata(bt_datafeed, timeframe=timeframe.bt_timeframe,
                                        compression=timeframe.bt_compression)
