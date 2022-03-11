import unittest
import datetime as dt

import backtrader as bt

from pyautofinance.common.engine import Engine, ComponentsAssembly
from pyautofinance.common.feeds import BackDatafeed
from pyautofinance.common.feeds.extractors import CCXTCandlesExtractor
from pyautofinance.common.datamodels import CSVDataModelsVisitor
from pyautofinance.common.brokers import BackBroker
from pyautofinance.common.sizers import Sizer
from pyautofinance.common.metrics import MetricsCollection, TotalGrossProfit
from pyautofinance.common.strategies import BracketStrategyExample, Strategy
from pyautofinance.common.timeframes import h4


class TestEngine(unittest.TestCase):

    start_date = dt.datetime(2020, 1, 1)
    end_date = dt.datetime(2021, 1, 1)
    symbol = 'BTC-EUR'
    timeframe = h4

    cash = 100000
    commission = 0.02

    visitor = CSVDataModelsVisitor()

    broker = BackBroker(cash, commission)
    strategy = Strategy(BracketStrategyExample)
    datafeed = BackDatafeed(symbol, start_date, timeframe, end_date, visitor, candles_extractor=CCXTCandlesExtractor())
    sizer = Sizer(bt.sizers.PercentSizer, percents=10)
    metrics = MetricsCollection([TotalGrossProfit])

    assembly = ComponentsAssembly(broker, strategy, datafeed, sizer, metrics)

    def test_initialization(self):
        engine = Engine(self.assembly)

    def test_run(self):
        engine = Engine(self.assembly)
        engine.run()


if __name__ == '__main__':
    unittest.main()
