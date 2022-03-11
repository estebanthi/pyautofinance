import datetime as dt
import unittest

from pyautofinance.common.timeframes import h4
from pyautofinance.common.datamodels.ohlcv import OHLCV
from pyautofinance.common.feeds.extractors import CCXTCandlesExtractor


class TestExtractors(unittest.TestCase):

    symbol = 'BTC-EUR'
    start_date = dt.datetime(2020, 1, 1)
    end_date = dt.datetime(2022, 1, 1)
    timeframe = h4
    ohlcv = OHLCV(symbol, start_date, end_date, timeframe)

    def test_extraction(self):
        extractor = CCXTCandlesExtractor()
        candles = extractor.extract_candles(self.ohlcv)
        last_date = candles.iloc[-1, 0]
        datetime = last_date.to_pydatetime()
        self.assertEqual(datetime, dt.datetime(2021, 12, 31, 21, 0, 0))


if __name__ == '__main__':
    unittest.main()
