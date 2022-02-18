import unittest

from enums.Market import Market
from enums.TimeFrame import TimeFrame
from feeds.datafeeds.BacktestingDatafeedGenerator import BacktestingDatafeedGenerator
from feeds.options.FeedOptions import FeedOptions
from feeds.options.MarketOptions import MarketOptions
from feeds.options.TimeOptions import TimeOptions
import datetime as dt
from feeds.extractors.CSVCandlesExtractor import CSVCandlesExtractor


class TestDatafeedsGenerators(unittest.TestCase):

    market_options = MarketOptions(Market.CRYPTO, "BNB-BTC")
    time_options = TimeOptions(dt.datetime(2020, 1, 1, 0, 0, 0), dt.datetime(2021, 1, 1, 0, 0, 0), TimeFrame.m5)
    feed_options = FeedOptions(market_options, time_options)

    def test_backtesting_datafeed(self):
        csv_candles_extractor = CSVCandlesExtractor()
        candles = csv_candles_extractor.extract_candles(self.feed_options)

        backtesting_datafeed_generator = BacktestingDatafeedGenerator()
        datafeed = backtesting_datafeed_generator.generate_backtesting_datafeed(candles, self.feed_options)
        print(datafeed)




if __name__ == '__main__':
    unittest.main()
