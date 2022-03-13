import datetime as dt
import unittest
import backtrader as bt

from pyautofinance.common.timeframes import h4
from pyautofinance.common.feeds import BackDatafeed
from pyautofinance.common.dataflux import DiskDataflux
from pyautofinance.common.exceptions import EndDateBeforeStartDate
from pyautofinance.common.feeds.extractors import CCXTCandlesExtractor


class TestBackDatafeed(unittest.TestCase):

    symbol = 'BTC-EUR'
    start_date = dt.datetime(2020, 1, 1)
    end_date = dt.datetime(2022, 1, 1)
    timeframe = h4
    dataflux = DiskDataflux()
    extractor = CCXTCandlesExtractor()

    def test_initialization(self):
        datafeed = BackDatafeed(self.symbol, self.start_date, self.timeframe, self.end_date, self.dataflux,
                                candles_extractor=self.extractor)
        bt_datafeed = datafeed._get_bt_datafeed()
        self.assertIsInstance(bt_datafeed, bt.feeds.DataBase)

    def test_wrong_dates(self):
        with self.assertRaises(EndDateBeforeStartDate):
            datafeed = BackDatafeed(self.symbol, self.end_date, self.timeframe, self.start_date, self.dataflux)


if __name__ == '__main__':
    unittest.main()
