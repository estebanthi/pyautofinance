import unittest
import backtrader as bt
import datetime as dt

from unittest.mock import patch

from pyautofinance.common.strategies.StrategiesFactory import StrategiesFactory
from pyautofinance.common.strategies.TestBracketStrategy import TestBracketStrategy
from pyautofinance.common.strategies.strat_loggers import DefaultStratLogger
from pyautofinance.common.feeds.extractors import CSVCandlesExtractor
from pyautofinance.common.options import FeedOptions, MarketOptions, TimeOptions, TimeFrame, Market
from pyautofinance.common.feeds.datafeeds_generators import BacktestingDatafeedGenerator


class TestStrategies(unittest.TestCase):

    def test_srategies_factory(self):
        factory = StrategiesFactory()
        strategy = TestBracketStrategy

        strategy_logging = factory.make_strategy(strategy, logging=True)
        self.assertEqual(strategy_logging, (TestBracketStrategy, {'logging': True}))

    @patch('builtins.print')
    def test_default_strat_logger(self, mock_print):
        time_options = TimeOptions(dt.datetime(2020, 1, 1), TimeFrame.d1, dt.datetime(2022, 1, 1))
        market_options = MarketOptions(Market.CRYPTO, "BTC-EUR")
        feed_options = FeedOptions(market_options, time_options)

        csv_extractor = CSVCandlesExtractor()
        candles = csv_extractor.get_formatted_and_filtered_candles(feed_options)

        datafeed_generator = BacktestingDatafeedGenerator()
        datafeed = datafeed_generator.generate_datafeed(candles, feed_options)

        strat_logger = DefaultStratLogger()
        strategy = TestBracketStrategy

        cerebro = bt.Cerebro()
        cerebro.adddata(datafeed)
        cerebro.addstrategy(strategy, logging=True)
        cerebro.run()



if __name__ == '__main__':
    unittest.main()
