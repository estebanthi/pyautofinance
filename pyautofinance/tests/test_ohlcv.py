import datetime as dt
import unittest

from pyautofinance.common.timeframes import h4
from pyautofinance.common.datamodels.ohlcv import OHLCV


class TestOHLCV(unittest.TestCase):

    symbol = 'BTC-EUR'
    start_date = dt.datetime(2020, 1, 1)
    end_date = dt.datetime(2022, 1, 1)
    timeframe = h4

    def test_initialization(self):
        ohlcv = OHLCV(self.symbol, self.start_date, self.end_date, self.timeframe)

    def test_ohlcv_to_str(self):
        ohlcv = OHLCV(self.symbol, self.start_date, self.end_date, self.timeframe)
        ohlcv_title = str(ohlcv)
        self.assertEqual(ohlcv_title, "BTC-EUR 2020-01-01 00-00-00 2022-01-01 00-00-00 4h")


if __name__ == '__main__':
    unittest.main()
