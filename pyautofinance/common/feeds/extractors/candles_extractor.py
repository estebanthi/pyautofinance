from abc import ABC, abstractmethod


class CandlesExtractor(ABC):

    def __init__(self, ohlcv):
        self._ohlcv = ohlcv
        self._symbol = ohlcv.symbol
        self._start_date = ohlcv.start_date
        self._end_date = ohlcv.end_date
        self._timeframe = ohlcv.timeframe

    @abstractmethod
    def extract_candles(self, symbol, start_date, end_date, timeframe):
        pass
