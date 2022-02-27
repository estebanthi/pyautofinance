import unittest
import backtrader as bt
import datetime as dt

from pyautofinance.common.engine.Engine import _Result
from pyautofinance.common.timeframes import h4
from pyautofinance.common.options import EngineOptions, MarketOptions, TimeOptions, FeedOptions, BrokerOptions,\
     Market
from pyautofinance.common.strategies.StrategiesFactory import StrategiesFactory
from pyautofinance.common.strategies.usable_strategies.TestBracketStrategy import TestBracketStrategy
from pyautofinance.common.sizers.SizersFactory import SizersFactory

from pyautofinance.common.analyzers.AnalyzersFactory import AnalyzersFactory
from pyautofinance.common.analyzers.FullMetrics import FullMetrics
from pyautofinance.common.testers.SplitTrainTestTester import SplitTrainTestTester


class TestTesters(unittest.TestCase):

    def test_percent_tester(self):
        market_options = MarketOptions(Market.CRYPTO, 'BTC-EUR')
        time_options = TimeOptions(dt.datetime(2020, 1, 1), h4(), dt.datetime(2022, 1, 1))
        feed_options = FeedOptions(market_options, time_options)

        broker_options = BrokerOptions(100_000, 0.2)

        strategy = StrategiesFactory().make_strategy(TestBracketStrategy, logging=False, stop_loss=range(2,4))
        sizer = SizersFactory().make_sizer(bt.sizers.PercentSizer, percents=10)

        tradeanalyzer = AnalyzersFactory().make_analyzer(bt.analyzers.TradeAnalyzer)
        fullmetrics = AnalyzersFactory().make_analyzer(FullMetrics, _name='full_metrics')

        engine_options = EngineOptions(broker_options, feed_options, [strategy], sizer,
                                       analyzers=[tradeanalyzer, fullmetrics],
                                       )

        tester = SplitTrainTestTester()
        test_result = tester.test(engine_options)
        self.assertEqual(type(test_result), _Result)


if __name__ == '__main__':
    unittest.main()
