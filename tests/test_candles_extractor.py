import datetime as dt
import unittest
import pandas as pd
from feeds.options.FeedOptions import FeedOptions
from feeds.options.MarketOptions import MarketOptions
from feeds.options.TimeOptions import TimeOptions
from enums.Market import Market
from enums.TimeFrame import TimeFrame
from feeds.extractors.CSVCandlesExtractor import CSVCandlesExtractor
from config.Config import Config
from feeds.extractors.CCXTCandlesExtractor import CCXTCandlesExtractor


class TestCandlesExtractor(unittest.TestCase):
    config = Config()
    datasets_pathname = config.get_datasets_pathname()

    test_feed_filename = "CRYPTO_BNB-BTC_01-01-2020_00-00-00_01-01-2021_00-00-00_m5.csv"
    test_candles = pd.read_csv(datasets_pathname + "/" + test_feed_filename)

    market_options = MarketOptions(Market.CRYPTO, "BNB-BTC")
    time_options = TimeOptions(dt.datetime(2020, 1, 1, 0, 0, 0), dt.datetime(2021, 1, 1, 0, 0, 0), TimeFrame.m5)
    feed_options = FeedOptions(market_options, time_options)

    def test_csv_candles_extractor(self):
        csv_candles_extractor = CSVCandlesExtractor(self.feed_options)
        candles = csv_candles_extractor.extract_candles()

        self.assertTrue(candles.equals(self.test_candles))

    def test_ccxt_candles_extractor(self):
        ccxt_candles_extractor = CCXTCandlesExtractor(self.feed_options)
        candles = ccxt_candles_extractor.extract_candles()
        print(candles)


if __name__ == '__main__':
    unittest.main()
