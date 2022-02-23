import unittest
import datetime as dt
import os
import backtrader as bt
import ccxt
from ccxtbt import CCXTFeed

from pyautofinance.common.options import BrokerOptions, EngineOptions, MarketOptions, TimeOptions, FeedOptions, TimeFrame, Market, WritingOptions
from pyautofinance.common.strategies.StrategiesFactory import StrategiesFactory
from pyautofinance.common.strategies.TestBracketStrategy import TestBracketStrategy
from pyautofinance.common.engine.Engine import Engine, RunningMode
from pyautofinance.common.feeds.FeedTitle import FeedTitle


class TestEngine(unittest.TestCase):

    def test_engine_correct_mode_chosen_1(self):
        broker_options = BrokerOptions(100_000, 0.2)

        market_options = MarketOptions(Market.CRYPTO, 'BTC-EUR')
        time_options = TimeOptions(dt.datetime(2020, 1, 1), TimeFrame.d1, dt.datetime(2022, 1, 1))
        feed_options = FeedOptions(market_options, time_options)

        strategies = [StrategiesFactory().make_strategy(TestBracketStrategy, logging=True)]

        engine_options = EngineOptions(broker_options, feed_options, strategies)

        engine = Engine(engine_options)

        self.assertEqual(engine._choose_running_mode(strategies), RunningMode.SIMPLE)

    def test_engine_correct_mode_chosen_2(self):
        broker_options = BrokerOptions(100_000, 0.2)

        market_options = MarketOptions(Market.CRYPTO, 'BTC-EUR')
        time_options = TimeOptions(dt.datetime(2020, 1, 1), TimeFrame.d1, dt.datetime(2022, 1, 1))
        feed_options = FeedOptions(market_options, time_options)

        strategies = [StrategiesFactory().make_strategy(TestBracketStrategy, logging=True, period=range(10))]

        engine_options = EngineOptions(broker_options, feed_options, strategies)

        engine = Engine(engine_options)

        self.assertEqual(engine._choose_running_mode(strategies), RunningMode.OPTIMIZED)

    def test_engine_correct_datafeed_pandas_data(self):
        broker_options = BrokerOptions(100_000, 0.2)

        market_options = MarketOptions(Market.CRYPTO, 'BTC-EUR')
        time_options = TimeOptions(dt.datetime(2020, 1, 1), TimeFrame.d1, dt.datetime(2021, 1, 1))
        feed_options = FeedOptions(market_options, time_options)

        strategies = [StrategiesFactory().make_strategy(TestBracketStrategy, logging=True, period=range(10))]

        engine_options = EngineOptions(broker_options, feed_options, strategies)

        engine = Engine(engine_options)

        candles = engine._get_candles(engine_options)
        datafeed = engine._get_datafeed(candles, engine_options)

        self.assertTrue(type(datafeed) == bt.feeds.PandasData)

    def test_engine_correct_datafeed_live_data(self):
        broker_options = BrokerOptions(currency='EUR', exchange=ccxt.binance())

        market_options = MarketOptions(Market.CRYPTO, 'BTC-EUR')
        time_options = TimeOptions(dt.datetime(2020, 1, 1), TimeFrame.d1)
        feed_options = FeedOptions(market_options, time_options)

        strategies = [StrategiesFactory().make_strategy(TestBracketStrategy, logging=True, period=range(10))]

        engine_options = EngineOptions(broker_options, feed_options, strategies)

        engine = Engine(engine_options)

        candles = engine._get_candles(engine_options)
        datafeed = engine._get_datafeed(candles, engine_options)
        self.assertTrue(type(datafeed) == CCXTFeed)

    def test_engine_write_candles(self):
        broker_options = BrokerOptions(100_000, 0.2)

        market_options = MarketOptions(Market.CRYPTO, 'BTC-EUR')
        time_options = TimeOptions(dt.datetime(2020, 1, 1), TimeFrame.d1, dt.datetime(2021, 1, 1))
        feed_options = FeedOptions(market_options, time_options)

        candles_destination = FeedTitle(feed_options).get_pathname()
        writing_options = WritingOptions(candles_destination)

        strategies = [StrategiesFactory().make_strategy(TestBracketStrategy, logging=True, period=range(10))]

        engine_options = EngineOptions(broker_options, feed_options, strategies, writing_options=writing_options)

        engine = Engine(engine_options)

        candles = engine._get_candles(engine_options)
        engine._write_candles_if_requested(candles, engine_options)

        self.assertTrue(os.path.isfile(candles_destination))

    def test_run_engine_optimized(self):
        broker_options = BrokerOptions(100_000, 0.2)

        market_options = MarketOptions(Market.CRYPTO, 'BTC-EUR')
        time_options = TimeOptions(dt.datetime(2020, 1, 1), TimeFrame.d1, dt.datetime(2021, 1, 1))
        feed_options = FeedOptions(market_options, time_options)

        strategies = [StrategiesFactory().make_strategy(TestBracketStrategy, longs_enabled=[True, False])]

        engine_options = EngineOptions(broker_options, feed_options, strategies)

        engine = Engine(engine_options)

        result = engine.run()
        self.assertEqual(type(result[0][0]), TestBracketStrategy)

    def test_run_engine_simple(self):
        broker_options = BrokerOptions(100_000, 0.2)

        market_options = MarketOptions(Market.CRYPTO, 'BTC-EUR')
        time_options = TimeOptions(dt.datetime(2020, 1, 1), TimeFrame.d1, dt.datetime(2021, 1, 1))
        feed_options = FeedOptions(market_options, time_options)

        strategies = [StrategiesFactory().make_strategy(TestBracketStrategy, longs_enabled=True)]

        engine_options = EngineOptions(broker_options, feed_options, strategies)

        engine = Engine(engine_options)

        result = engine.run()
        self.assertEqual(type(result[0]), TestBracketStrategy)



if __name__ == '__main__':
    unittest.main()