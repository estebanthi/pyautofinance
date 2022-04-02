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
        self.end_date = end_date
        self.dataflux = dataflux
        self.timeframe = timeframe
        self.ohlcv = OHLCV(self.symbol, self.start_date, self.end_date, self.timeframe)
        self.filterer = candles_filterer
        self.formatter = candles_formatter
        self.candles_extractor = candles_extractor
        self._check_dates_are_correct()

    def _check_dates_are_correct(self):
        if self.end_date:
            if self.end_date < self.start_date:
                raise EndDateBeforeStartDate

    def _get_bt_datafeed(self) -> bt.DataBase:
        self._load_ohlcv()
        dataframe = self.ohlcv.dataframe
        formatted_dataframe = self.formatter.format_candles(dataframe)
        filtered_dataframe = self.filterer.filter_candles(formatted_dataframe)
        return bt.feeds.PandasData(dataname=filtered_dataframe, timeframe=self.timeframe.bt_timeframe,
                                   compression=self.timeframe.bt_compression, datetime=0)

    def _load_ohlcv(self):
        self.ohlcv = OHLCV(self.symbol, self.start_date, self.end_date, self.timeframe)
        if not self.dataflux.check(self.ohlcv):
            if not self.candles_extractor:
                raise NoExtractor
            candles = self.candles_extractor.extract_candles(self.ohlcv)
            self.ohlcv.dataframe = candles
            self.dataflux.write(self.ohlcv)
        else:
            self.dataflux.load(self.ohlcv)

    def get_ohlcv(self):
        return self.ohlcv

    def extract(self):
        self._load_ohlcv()
