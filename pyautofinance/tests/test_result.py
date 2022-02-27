import unittest
import backtrader as bt
import datetime as dt

from pyautofinance.common.engine.Engine import Engine
from pyautofinance.common.timeframes import h4
from pyautofinance.common.options import EngineOptions, MarketOptions, TimeOptions, FeedOptions, BrokerOptions,\
     Market
from pyautofinance.common.strategies.StrategiesFactory import StrategiesFactory
from pyautofinance.common.strategies.usable_strategies.TestBracketStrategy import TestBracketStrategy
from pyautofinance.common.sizers.SizersFactory import SizersFactory

from pyautofinance.common.metrics import TotalGrossProfit, MetricsCollection


class TestResult(unittest.TestCase):

    def test_result(self):
        market_options = MarketOptions(Market.CRYPTO, 'BTC-EUR')
        time_options = TimeOptions(dt.datetime(2020, 1, 1), h4(), dt.datetime(2022, 1, 1))
        feed_options = FeedOptions(market_options, time_options)

        broker_options = BrokerOptions(100_000, 0.2)

        strategy = StrategiesFactory().make_strategy(TestBracketStrategy, logging=False, stop_loss=range(3,5))
        sizer = SizersFactory().make_sizer(bt.sizers.PercentSizer, percents=10)

        metrics = [TotalGrossProfit]
        engine_options = EngineOptions(broker_options, feed_options, [strategy], sizer, metrics=metrics)

        engine = Engine(engine_options)
        result = engine.run()

        print(result['BTC-EUR'])

        self.assertEqual(type(result['BTC-EUR'][0][0]), MetricsCollection)


if __name__ == '__main__':
    unittest.main()
