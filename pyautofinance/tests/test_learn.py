import unittest
import datetime as dt

import pandas_ta as ta
import pandas as pd

from pyautofinance.common.feeds import BackDatafeed
from pyautofinance.common.feeds.extractors import CCXTCandlesExtractor
from pyautofinance.common.dataflux import DiskDataflux
from pyautofinance.common.timeframes import h1
from sklearn.ensemble import RandomForestClassifier
from pyautofinance.common.learn import TaLibPredicter
from pyautofinance.common.learn import FullTester


class TestLearn(unittest.TestCase):

    start_date = dt.datetime(2020, 1, 1)
    end_date = dt.datetime(2022, 1, 1)
    symbol = 'BTC-EUR'
    timeframe = h1

    cash = 100000
    commission = 0.02

    dataflux = DiskDataflux()

    datafeed = BackDatafeed(symbol, start_date, timeframe, end_date, dataflux, candles_extractor=CCXTCandlesExtractor())
    datafeed2 = BackDatafeed(symbol, dt.datetime(2022, 1, 1), timeframe, dt.datetime(2022, 3, 18), dataflux,
                             candles_extractor=CCXTCandlesExtractor())

    clf = RandomForestClassifier()
    predicter = TaLibPredicter(clf, ta.AllStrategy)

    def test_fit(self):
        self.predicter.fit(self.datafeed)

    def test_get_real_outputs(self):
        self.assertTrue(isinstance(self.predicter.get_real_outputs(self.datafeed), pd.Series))

    def test_validator(self):
        tester = FullTester(self.predicter)
        tester.test(self.datafeed2)


if __name__ == '__main__':
    unittest.main()
