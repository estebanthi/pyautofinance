import unittest
from feeds.writers.CSVCandlesWriter import CSVCandlesWriter
from feeds.extractors.CSVCandlesExtractor import CSVCandlesExtractor
import datetime as dt
from feeds.options.FeedOptions import FeedOptions
from feeds.options.TimeOptions import TimeOptions
from feeds.options.MarketOptions import MarketOptions
from enums.Market import Market
from enums.TimeFrame import TimeFrame
from feeds.FeedTitle import FeedTitle
import os


class TestTimeOptions(unittest.TestCase):

    writer = CSVCandlesWriter()
    extractor = CSVCandlesExtractor()

    market_options = MarketOptions(Market.CRYPTO, "BNB-BTC")
    time_options = TimeOptions(dt.datetime(2020, 1, 1, 0, 0, 0), dt.datetime(2021, 1, 1, 0, 0, 0), TimeFrame.m5)
    feed_options = FeedOptions(market_options, time_options)

    def test_writing(self):
        feed_title = FeedTitle(self.feed_options)
        feed_pathname = feed_title.get_pathname()
        feed_pathname += "_test.csv"

        os.remove(feed_pathname)

        candles = self.extractor.extract_candles(self.feed_options)
        self.writer.write(candles, feed_pathname)

        self.assertTrue(os.path.isfile(feed_pathname))


if __name__ == '__main__':
    unittest.main()
