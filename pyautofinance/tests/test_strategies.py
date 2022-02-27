import unittest
import backtrader as bt
import datetime as dt

from unittest.mock import patch
from collections import namedtuple

from pyautofinance.common.strategies.StrategiesFactory import StrategiesFactory, StrategyType, Strategy
from pyautofinance.common.strategies._BracketStrategy import _BracketStrategy
from pyautofinance.common.strategies.strat_loggers import DefaultStratLogger
from pyautofinance.common.feeds.extractors import CSVCandlesExtractor
from pyautofinance.common.options import FeedOptions, MarketOptions, TimeOptions, Market
from pyautofinance.common.timeframes import d1
from pyautofinance.common.feeds.datafeeds_generators import BacktestingDatafeedGenerator


class TestStrategies(unittest.TestCase):

    def test_simple_strategy(self):
        factory = StrategiesFactory()
        strategy = _BracketStrategy

        strategy_logging = factory.make_strategy(strategy, logging=True)
        self.assertEqual(strategy_logging, Strategy(_BracketStrategy, StrategyType.SIMPLE, {'logging': True}))

    def test_optimized_strategy(self):
        factory = StrategiesFactory()
        strategy = _BracketStrategy

        strategy_logging = factory.make_strategy(strategy, logging=True, period=range(10))
        self.assertEqual(strategy_logging,
                         Strategy(_BracketStrategy, StrategyType.OPTIMIZED, {'logging': True, 'period': range(10)}))

    @patch('builtins.print')
    def test_default_strat_logger(self, mock_print):
        time_options = TimeOptions(dt.datetime(2020, 1, 1), d1(), dt.datetime(2022, 1, 1))
        market_options = MarketOptions(Market.CRYPTO, "BTC-EUR")
        feed_options = FeedOptions(market_options, time_options)

        csv_extractor = CSVCandlesExtractor()
        candles = csv_extractor.get_formatted_and_filtered_candles(feed_options)

        datafeed_generator = BacktestingDatafeedGenerator()
        datafeed = datafeed_generator.generate_datafeed(candles, feed_options)

        strat_logger = DefaultStratLogger()
        strategy = _BracketStrategy

        cerebro = bt.Cerebro()
        cerebro.adddata(datafeed)
        cerebro.addstrategy(strategy, logging=True)
        cerebro.run()



if __name__ == '__main__':
    unittest.main()
