import unittest
import datetime as dt

import backtrader as bt
from sklearn.ensemble import RandomForestClassifier
import pandas_ta as ta

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
from pyautofinance.common.testers import ClassificationTester
from pyautofinance.common.learn import TaLibPredicter
from pyautofinance.common.results.test_results_collection import TestResultsCollection
from pyautofinance.common.testers import SplitTrainTestTester, WalkForwardTester, MonkeyTester
from pyautofinance.common.strategies.test_strats.monkey_strat import MonkeyStrat


class TestTesters(unittest.TestCase):

    start_date = dt.datetime(2020, 1, 1)
    end_date = dt.datetime(2021, 1, 1)
    symbol = 'BTC-EUR'
    timeframe = h4

    cash = 100000
    commission = 0.02

    dataflux = DiskDataflux()

    broker = BackBroker(cash, commission)
    strategy = Strategy(BracketStrategyExample, stop_loss=range(2, 4), risk_reward=range(2, 4))
    datafeed = BackDatafeed(symbol, start_date, timeframe, end_date, dataflux, candles_extractor=CCXTCandlesExtractor())
    sizer = Sizer(bt.sizers.PercentSizer, percents=90)
    metrics = EngineMetricsCollection(TotalGrossProfit)

    assembly = ComponentsAssembly(broker, strategy, datafeed, sizer, metrics)

    model = RandomForestClassifier()
    strategy = ta.AllStrategy
    predicter = TaLibPredicter(model, strategy)

    def test_monte_carlo_tester(self):
        engine = Engine(self.assembly)
        tester = MonteCarloTester(1000, 100000, 50000)
        result = tester.test(engine)
        self.assertIsInstance(result, TestResultsCollection)

    def test_classification_tester(self):
        engine = Engine(self.assembly)
        self.predicter.fit(engine.components_assembly[2])
        tester = ClassificationTester(self.predicter)
        result = tester.test(engine)
        self.assertIsInstance(result, TestResultsCollection)

    def test_split_train_test_tester(self):
        engine = Engine(self.assembly)
        tester = SplitTrainTestTester()
        result = tester.test(engine)
        self.assertIsInstance(result, TestResultsCollection)

    def test_walk_forward_tester(self):
        engine = Engine(self.assembly)
        tester = WalkForwardTester()
        result = tester.test(engine)
        self.assertIsInstance(result, TestResultsCollection)

    def test_monkey_tester(self):
        engine = Engine(self.assembly)
        monkey_full = Strategy(MonkeyStrat)
        tester = MonkeyTester(monkey_full, 2)

        result = tester.test(engine)
        print(result.validate(['ProfitDifference'], [lambda x: x > 0]))


if __name__ == '__main__':
    unittest.main()
