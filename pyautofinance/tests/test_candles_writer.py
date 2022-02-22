import unittest
import os
import datetime as dt

from pyautofinance.common.options import FeedOptions, MarketOptions, TimeOptions, Market, TimeFrame

from pyautofinance.common.feeds.FeedTitle import FeedTitle
from pyautofinance.common.feeds.extractors import CSVCandlesExtractor

from pyautofinance.common.feeds.writers import CandlesWriter


class TestWriting(unittest.TestCase):

    writer = CandlesWriter()
    extractor = CSVCandlesExtractor()

    market_options = MarketOptions(Market.CRYPTO, "BTC-EUR")
    time_options = TimeOptions(dt.datetime(2020, 1, 1, 0, 0, 0), dt.datetime(2020, 3, 1, 0, 0, 0), TimeFrame.d1)
    feed_options = FeedOptions(market_options, time_options)

    def test_writing(self):
        feed_title = FeedTitle(self.feed_options)
        feed_pathname = feed_title.get_pathname()

        candles = self.extractor.get_formatted_and_filtered_candles(self.feed_options)
        self.writer.write(candles, feed_pathname)

        self.assertTrue(os.path.isfile(feed_pathname))


if __name__ == '__main__':
    unittest.main()
