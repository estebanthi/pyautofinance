import unittest
import datetime as dt

import backtrader as bt

from pyautofinance.common.engine import Engine, ComponentsAssembly
from pyautofinance.common.feeds import BackDatafeed
from pyautofinance.common.feeds.extractors import CCXTCandlesExtractor
from pyautofinance.common.dataflux import DiskDataflux
from pyautofinance.common.brokers import BackBroker
from pyautofinance.common.sizers import Sizer
from pyautofinance.common.metrics.engine_metrics import EngineMetricsCollection, TotalGrossProfit
from pyautofinance.common.strategies import BracketStrategyExample, Strategy
from pyautofinance.common.timeframes import h4
from pyautofinance.common.testers import MonteCarloTester
from pyautofinance.common.metrics.miscellaneous_metrics import RiskOfRuin


class TestTesters(unittest.TestCase):

    start_date = dt.datetime(2020, 1, 1)
    end_date = dt.datetime(2021, 1, 1)
    symbol = 'BTC-EUR'
    timeframe = h4

    cash = 100000
    commission = 0.02

    dataflux = DiskDataflux()

    broker = BackBroker(cash, commission)
    strategy = Strategy(BracketStrategyExample, stop_loss=2, risk_reward=2)
    datafeed = BackDatafeed(symbol, start_date, timeframe, end_date, dataflux, candles_extractor=CCXTCandlesExtractor())
    sizer = Sizer(bt.sizers.PercentSizer, percents=90)
    metrics = EngineMetricsCollection(TotalGrossProfit)

    assembly = ComponentsAssembly(broker, strategy, datafeed, sizer, metrics)

    def test(self):
        engine = Engine(self.assembly)
        result = engine.run()
        tester = MonteCarloTester(1000, 100000, 50000)
        test_results_collection = tester.test(result)
        test_results_collection[0]['RiskOfRuin']

    def test_validation_metric(self):
        engine = Engine(self.assembly)
        result = engine.run()
        tester = MonteCarloTester(1000, 100000, 50000)
        test_results_collection = tester.test(result)

        metric_1 = RiskOfRuin
        validation_function_1 = lambda risk_of_ruin: risk_of_ruin < 0.3

        metric_2 = RiskOfRuin
        validation_function_2 = lambda risk_of_ruin: risk_of_ruin > 0.3

        metrics = [metric_1, metric_2]
        validation_functions = [validation_function_1, validation_function_2]

        validations = test_results_collection.validate(metrics, validation_functions)
        self.assertIsInstance(validations, dict)


if __name__ == '__main__':
    unittest.main()
