import unittest
import datetime as dt
import pandas as pd

from pyautofinance.common.options import FeedOptions, MarketOptions, TimeOptions, Market, TimeFrame

from pyautofinance.common.config import Config

from pyautofinance.common.feeds.extractors import CSVCandlesExtractor, CCXTCandlesExtractor
from pyautofinance.common.feeds.formatters import SimpleCandlesFormatter
from pyautofinance.common.feeds.filterers import SimpleCandlesFilterer


class TestCandlesExtractor(unittest.TestCase):
    config = Config()
    datasets_pathname = config.get_datasets_pathname()

    test_feed_filename = "CRYPTO_BTC-EUR_2020-01-01_00-00-00_2020-03-01_00-00-00_d1.csv"
    test_candles = pd.read_csv(datasets_pathname + "/" + test_feed_filename)

    market_options = MarketOptions(Market.CRYPTO, "BTC-EUR")
    time_options = TimeOptions(dt.datetime(2020, 1, 1, 0, 0, 0), end_date=dt.datetime(2020, 3, 1, 0, 0, 0), timeframe=TimeFrame.d1)
    feed_options = FeedOptions(market_options, time_options)

    formatter = SimpleCandlesFormatter()
    formatted_test_candles = formatter.format_candles(test_candles, feed_options)

    filterer = SimpleCandlesFilterer()
    formatted_and_filtered_test_candles = filterer.filter_candles(formatted_test_candles, feed_options)

    def test_csv_candles_extractor(self):
        csv_candles_extractor = CSVCandlesExtractor()
        candles = csv_candles_extractor.get_formatted_and_filtered_candles(self.feed_options)

        self.assertTrue(candles["Close"].equals(self.formatted_and_filtered_test_candles["Close"]))

    def test_ccxt_candles_extractor(self):
        ccxt_candles_extractor = CCXTCandlesExtractor()
        candles = ccxt_candles_extractor.get_formatted_and_filtered_candles(self.feed_options)

        csv_candles_extractor = CSVCandlesExtractor()
        csv_candles = csv_candles_extractor.get_formatted_and_filtered_candles(self.feed_options)

        self.assertTrue(candles["Close"].equals(csv_candles["Close"]))

# TOO LONG TO EXECUTE
    def test_ccxt_limit_bypass(self):
        ccxt_candles_extractor = CCXTCandlesExtractor()
        time_options = TimeOptions(dt.datetime(2020, 1, 1, 0, 0, 0), end_date=dt.datetime(2021, 6, 1, 0, 0, 0),
                                   timeframe=TimeFrame.h1)
        feed_options = FeedOptions(self.market_options, time_options)
        candles = ccxt_candles_extractor.get_formatted_and_filtered_candles(feed_options)

        csv_candles_extractor = CSVCandlesExtractor()
        csv_candles = csv_candles_extractor.get_formatted_and_filtered_candles(feed_options)

        self.assertTrue(candles["Close"].equals(csv_candles["Close"]))


if __name__ == '__main__':
    unittest.main()
