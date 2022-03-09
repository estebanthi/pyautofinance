import datetime as dt
import unittest

from pyautofinance.common.timeframes import h4, h1, h2
from pyautofinance.common.datamodels import OHLCV
from pyautofinance.common.datamodels import CSVDataModelsVisitor


class TestDatamodelsVisitors(unittest.TestCase):

    symbol = 'BTC-EUR'
    start_date = dt.datetime(2020, 1, 1)
    end_date = dt.datetime(2022, 1, 1)
    timeframe = h4
    timeframe2 = h1
    timeframe3 = h2

    def test_check_ohlcv_false(self):
        visitor = CSVDataModelsVisitor()
        ohlcv = OHLCV(self.symbol, self.start_date, self.end_date, self.timeframe3)
        self.assertEqual(visitor.check_ohlcv(ohlcv), False)

    def test_check_ohlcv_true(self):
        visitor = CSVDataModelsVisitor()
        ohlcv = OHLCV(self.symbol, self.start_date, self.end_date, self.timeframe)
        self.assertEqual(visitor.check_ohlcv(ohlcv), True)

    def test_load_ohlcv(self):
        visitor = CSVDataModelsVisitor()
        ohlcv = OHLCV(self.symbol, self.start_date, self.end_date, self.timeframe)
        visitor.load_ohlcv(ohlcv)
        self.assertTrue(len(ohlcv.dataframe) > 0)

    def test_save_ohlcv(self):
        visitor = CSVDataModelsVisitor()
        ohlcv = OHLCV(self.symbol, self.start_date, self.end_date, self.timeframe2)
        visitor.save_ohlcv(ohlcv)


if __name__ == '__main__':
    unittest.main()
