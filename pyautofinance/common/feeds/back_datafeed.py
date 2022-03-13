import backtrader as bt

from pyautofinance.common.feeds.datafeed import Datafeed
from pyautofinance.common.exceptions import EndDateBeforeStartDate, NoExtractor
from pyautofinance.common.datamodels.ohlcv import OHLCV
from pyautofinance.common.feeds.formatters import DefaultCandlesFormatter
from pyautofinance.common.feeds.filterers import DefaultCandlesFilterer


class BackDatafeed(Datafeed):

    def __init__(self, symbol, start_date, timeframe, end_date, dataflux,
                 candles_formatter=DefaultCandlesFormatter(), candles_filterer=DefaultCandlesFilterer(),
                 candles_extractor=None):
        super().__init__(symbol, start_date, timeframe)
        self._end_date = end_date
        self._dataflux = dataflux
        self._ohlcv = OHLCV(symbol, start_date, end_date, timeframe)
        self._filterer = candles_filterer
        self._formatter = candles_formatter
        self._candles_extractor = candles_extractor
        self._check_dates_are_correct()

    def _check_dates_are_correct(self):
        if self._end_date:
            if self._end_date < self._start_date:
                raise EndDateBeforeStartDate

    def _get_bt_datafeed(self) -> bt.DataBase:
        self._load_ohlcv()
        dataframe = self._ohlcv.dataframe
        formatted_dataframe = self._formatter.format_candles(dataframe)
        filtered_dataframe = self._filterer.filter_candles(formatted_dataframe)

        return bt.feeds.PandasData(dataname=filtered_dataframe, timeframe=self._timeframe.bt_timeframe,
                                   compression=self._timeframe.bt_compression, datetime=0)

    def _load_ohlcv(self):
        if not self._dataflux.check(self._ohlcv):
            if not self._candles_extractor:
                raise NoExtractor
            candles = self._candles_extractor.extract_candles(self._ohlcv)
            self._ohlcv.dataframe = candles
            self._dataflux.write(self._ohlcv)
        else:
            self._dataflux.load(self._ohlcv)
