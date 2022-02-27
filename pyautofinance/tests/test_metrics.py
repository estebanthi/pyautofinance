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

from pyautofinance.common.metrics import TotalGrossProfit


class TestMetrics(unittest.TestCase):

    def test_metrics(self):
        market_options = MarketOptions(Market.CRYPTO, 'BTC-EUR')
        time_options = TimeOptions(dt.datetime(2020, 1, 1), h4(), dt.datetime(2022, 1, 1))
        feed_options = FeedOptions(market_options, time_options)

        broker_options = BrokerOptions(100_000, 0.2)

        strategy = StrategiesFactory().make_strategy(TestBracketStrategy, logging=False, stop_loss=range(2,4))
        sizer = SizersFactory().make_sizer(bt.sizers.PercentSizer, percents=10)

        metrics = [TotalGrossProfit()]
        engine_options = EngineOptions(broker_options, feed_options, [strategy], sizer, metrics=metrics)

        engine = Engine(engine_options)
        analyzers_from_metrics = engine._get_analyzers_from_metrics(engine_options)
        self.assertEqual(type(analyzers_from_metrics[0]), bt.MetaAnalyzer)


if __name__ == '__main__':
    unittest.main()
