import backtrader as bt

from pyautofinance.common.feeds.datafeed import Datafeed
from pyautofinance.common.exceptions import EndDateBeforeStartDate
from pyautofinance.common.datamodels.ohlcv import OHLCV


class BackDatafeed(Datafeed):

    def __init__(self, symbol, start_date, timeframe, end_date, datamodels_visitor, candles_extractor=None):
        super().__init__(symbol, start_date, timeframe)
        self._end_date = end_date
        self._datamodels_visitor = datamodels_visitor
        self._ohlcv = OHLCV(symbol, start_date, end_date, timeframe)

        if candles_extractor:
            self._candles_extractor = candles_extractor(self._ohlcv)

        self._check_dates_are_correct()

        self._load_ohlcv()
        dataframe = self._ohlcv.dataframe
        self._datafeed = bt.feeds.PandasData(dataname=dataframe, timeframe=timeframe.bt_timeframe,
                                       compression=timeframe.bt_compression, datetime=0)

    def _check_dates_are_correct(self):
        if self._end_date:
            if self._end_date < self._start_date:
                raise EndDateBeforeStartDate

    def _load_ohlcv(self):
        if not self._ohlcv.accept_visitor_check(self._datamodels_visitor):
            candles = self._candles_extractor.extract_candles(self._ohlcv)
            self._ohlcv.dataframe = candles
            self._ohlcv.accept_visitor_save(self._datamodels_visitor)
        else:
            self._ohlcv.accept_visitor_load(self._datamodels_visitor)
