import unittest
import datetime as dt

from pyautofinance.common.options import FeedOptions, MarketOptions, TimeOptions, Market, TimeFrame

from pyautofinance.common.feeds.FeedTitle import FeedTitle

from pyautofinance.common.config import Config


class TestFeedTitle(unittest.TestCase):

    config = Config()
    datasets_pathname = config.get_datasets_pathname()

    test_feed_filename = "CRYPTO_BNB-BTC_01-01-2020_00-00-00_01-01-2021_00-00-00_m5.csv"

    market_options = MarketOptions(Market.CRYPTO, "BNB-BTC")
    time_options = TimeOptions(dt.datetime(2020, 1, 1, 0, 0, 0), dt.datetime(2021, 1, 1, 0, 0, 0), TimeFrame.m5)
    feed_options = FeedOptions(market_options, time_options)

    def test_feed_name(self):
        feed_title = FeedTitle(self.feed_options)
        feed_filename = feed_title.get_filename()

        self.assertEqual(feed_filename, self.test_feed_filename)

    def test_feed_pathname(self):
        feed_title = FeedTitle(self.feed_options)
        feed_pathname = feed_title.get_pathname()

        test_feed_pathname = self.datasets_pathname + "/" + self.test_feed_filename

        self.assertEqual(feed_pathname, test_feed_pathname)


if __name__ == '__main__':
    unittest.main()
