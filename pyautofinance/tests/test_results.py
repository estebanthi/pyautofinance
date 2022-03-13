import unittest
import datetime as dt

import backtrader as bt

from pyautofinance.common.engine import Engine, ComponentsAssembly
from pyautofinance.common.feeds import BackDatafeed
from pyautofinance.common.feeds.extractors import CCXTCandlesExtractor
from pyautofinance.common.datamodels.feeds_visitors import CSVFeedsVisitors
from pyautofinance.common.brokers import BackBroker
from pyautofinance.common.sizers import Sizer
from pyautofinance.common.metrics import MetricsCollection, TotalGrossProfit
from pyautofinance.common.strategies import BracketStrategyExample, Strategy
from pyautofinance.common.timeframes import h4
from pyautofinance.common.results.strat_result import StratResult


class TestResults(unittest.TestCase):

    start_date = dt.datetime(2020, 1, 1)
    end_date = dt.datetime(2021, 1, 1)
    symbol = 'BTC-EUR'
    timeframe = h4

    cash = 100000
    commission = 0.02

    visitor = CSVFeedsVisitors()

    broker = BackBroker(cash, commission)
    strategy = Strategy(BracketStrategyExample, stop_loss=[0.5, 1], risk_reward=2)
    datafeed = BackDatafeed(symbol, start_date, timeframe, end_date, visitor, candles_extractor=CCXTCandlesExtractor())
    sizer = Sizer(bt.sizers.PercentSizer, percents=10)
    metrics = MetricsCollection([TotalGrossProfit])

    assembly = ComponentsAssembly(broker, strategy, datafeed, sizer, metrics)

    def test_engine_result(self):
        engine = Engine(self.assembly)
        result = engine.run()
        for strat in result:
            self.assertTrue(isinstance(strat, StratResult))

    def test_get_metric(self):
        engine = Engine(self.assembly)
        result = engine.run()
        result[0].get_metric("TotalGrossProfit")

    def test_get_best_params(self):
        engine = Engine(self.assembly)
        result = engine.run()
        print(result.get_best_params('TotalGrossProfit'))


if __name__ == '__main__':
    unittest.main()
