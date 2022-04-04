import unittest
import datetime as dt

import backtrader as bt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pandas_ta as ta

from pyautofinance.common.engine import Engine, ComponentsAssembly
from pyautofinance.common.feeds import BackDatafeed
from pyautofinance.common.feeds.extractors import CCXTCandlesExtractor
from pyautofinance.common.dataflux import DiskDataflux
from pyautofinance.common.brokers import BackBroker
from pyautofinance.common.sizers import Sizer
from pyautofinance.common.metrics.engine_metrics import EngineMetricsCollection, TotalGrossProfit, TotalNetProfit
from pyautofinance.common.strategies import BracketStrategyExample, Strategy
from pyautofinance.common.timeframes import h4
from pyautofinance.common.learn import TaLibPredicter
from pyautofinance.common.testers import ClassificationTester
from pyautofinance.common.metrics.metric import Metric


class TestLearn(unittest.TestCase):
    start_date = dt.datetime(2020, 1, 1)
    end_date = dt.datetime(2021, 1, 1)
    symbol = 'BTC-EUR'
    timeframe = h4

    cash = 100000
    commission = 0.02

    dataflux = DiskDataflux()

    broker = BackBroker(cash, commission)
    strategy = Strategy(BracketStrategyExample, stop_loss=[0.5, 1], risk_reward=2)
    datafeed = BackDatafeed(symbol, start_date, timeframe, end_date, dataflux, candles_extractor=CCXTCandlesExtractor())
    sizer = Sizer(bt.sizers.PercentSizer, percents=10)
    metrics = EngineMetricsCollection(TotalGrossProfit, TotalNetProfit)

    assembly = ComponentsAssembly(broker, strategy, datafeed, sizer, metrics)
    engine = Engine(assembly)
    engine_result = engine.run()
    origin_datafeed = engine_result.datafeed

    model = RandomForestClassifier()
    strategy = ta.AllStrategy
    predicter = TaLibPredicter(model, strategy)

    def test_fit(self):
        self.predicter.fit(self.origin_datafeed)

    def test_get_real_outputs(self):
        self.assertTrue(isinstance(self.predicter.get_real_outputs(self.origin_datafeed), pd.Series))


if __name__ == '__main__':
    unittest.main()
