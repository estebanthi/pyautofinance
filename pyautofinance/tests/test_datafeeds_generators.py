import unittest
import datetime as dt

from pyautofinance.common.options import FeedOptions, MarketOptions, TimeOptions, Market, TimeFrame

from pyautofinance.common.feeds.extractors import CSVCandlesExtractor

from pyautofinance.common.feeds.datafeeds_generators import BacktestingDatafeedGenerator


class TestDatafeedsGenerators(unittest.TestCase):

    market_options = MarketOptions(Market.CRYPTO, "BNB-BTC")
    time_options = TimeOptions(dt.datetime(2020, 1, 1, 0, 0, 0), dt.datetime(2021, 1, 1, 0, 0, 0), TimeFrame.m5)
    feed_options = FeedOptions(market_options, time_options)

    def test_backtesting_datafeed(self):
        csv_candles_extractor = CSVCandlesExtractor()
        candles = csv_candles_extractor.get_formatted_and_filtered_candles(self.feed_options)

        backtesting_datafeed_generator = BacktestingDatafeedGenerator()
        datafeed = backtesting_datafeed_generator.generate_datafeed(candles, self.feed_options)


if __name__ == '__main__':
    unittest.main()
