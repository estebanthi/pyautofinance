import datetime as dt
import unittest

from pyautofinance.common.timeframes import h4, h1, h2
from pyautofinance.common.datamodels.ohlcv import OHLCV
from pyautofinance.common.dataflux import DiskDataflux


class TestDatamodelsVisitors(unittest.TestCase):

    symbol = 'BTC-EUR'
    start_date = dt.datetime(2020, 1, 1)
    end_date = dt.datetime(2022, 1, 1)
    timeframe = h4
    timeframe2 = h1
    timeframe3 = h2

    def test_check_ohlcv_false(self):
        dataflux = DiskDataflux()
        ohlcv = OHLCV(self.symbol, self.start_date, self.end_date, self.timeframe3)
        self.assertEqual(dataflux.check(ohlcv), False)

    def test_check_ohlcv_true(self):
        dataflux = DiskDataflux()
        ohlcv = OHLCV(self.symbol, self.start_date, self.end_date, self.timeframe)
        self.assertEqual(dataflux.check(ohlcv), True)

    def test_load_ohlcv(self):
        dataflux = DiskDataflux()
        ohlcv = OHLCV(self.symbol, self.start_date, self.end_date, self.timeframe)
        dataflux.load(ohlcv)
        self.assertTrue(len(ohlcv.dataframe) > 0)

    def test_save_ohlcv(self):
        dataflux = DiskDataflux()
        ohlcv = OHLCV(self.symbol, self.start_date, self.end_date, self.timeframe2)
        dataflux.write(ohlcv)


if __name__ == '__main__':
    unittest.main()
