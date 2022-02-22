import unittest
import datetime as dt

from ccxt import binance

from pyautofinance.common.options import FeedOptions, MarketOptions, BrokerOptions, TimeOptions, Market, TimeFrame

from pyautofinance.common.feeds.extractors import CSVCandlesExtractor

from pyautofinance.common.feeds.datafeeds_generators import BacktestingDatafeedGenerator, CryptoLiveDatafeedGenerator


class TestDatafeedsGenerators(unittest.TestCase):

    market_options = MarketOptions(Market.CRYPTO, "BTC-EUR")
    time_options = TimeOptions(dt.datetime(2020, 1, 1, 0, 0, 0), end_date=dt.datetime(2020, 3, 1, 0, 0, 0), timeframe=TimeFrame.d1)
    feed_options = FeedOptions(market_options, time_options)

    live_time_options = TimeOptions(dt.datetime(2022, 1, 1), end_date=dt.datetime(2022, 2, 1), timeframe=TimeFrame.d1)
    live_feed_options = FeedOptions(market_options, time_options)
    live_exchange_options = BrokerOptions(exchange=binance(), currency="EUR")

    def test_backtesting_datafeed(self):
        csv_candles_extractor = CSVCandlesExtractor()
        candles = csv_candles_extractor.get_formatted_and_filtered_candles(self.feed_options)

        backtesting_datafeed_generator = BacktestingDatafeedGenerator()
        datafeed = backtesting_datafeed_generator.generate_datafeed(candles, self.feed_options)

    def test_live_datafeed(self):
        live_datafeed_generator = CryptoLiveDatafeedGenerator()
        datafeed = live_datafeed_generator.generate_datafeed(self.live_feed_options, self.live_exchange_options)


if __name__ == '__main__':
    unittest.main()
