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
from pyautofinance.common.simulators import WalkForwardSimulator


class TestWalkForwardSimulator(unittest.TestCase):

    def test_normal(self):
        start_date = dt.datetime(2020, 1, 1)
        end_date = dt.datetime(2022, 1, 1)
        symbol = 'BTC-EUR'
        timeframe = h4

        cash = 100000
        commission = 0.02

        dataflux = DiskDataflux()
        broker = BackBroker(cash, commission)
        strategy = Strategy(BracketStrategyExample, stop_loss=2, risk_reward=2)
        datafeed = BackDatafeed(symbol, start_date, timeframe, end_date, dataflux,
                                candles_extractor=CCXTCandlesExtractor())
        sizer = Sizer(bt.sizers.PercentSizer, percents=90)
        metrics = EngineMetricsCollection(TotalGrossProfit)
        assembly = ComponentsAssembly(broker, strategy, datafeed, sizer, metrics)
        engine = Engine(assembly)
        simulator = WalkForwardSimulator(periods=2)
        result = simulator.simulate(engine)

    def test_anchored(self):
        start_date = dt.datetime(2020, 1, 1)
        end_date = dt.datetime(2022, 1, 1)
        symbol = 'BTC-EUR'
        timeframe = h4

        cash = 100000
        commission = 0.02

        dataflux = DiskDataflux()
        broker = BackBroker(cash, commission)
        strategy = Strategy(BracketStrategyExample, stop_loss=2, risk_reward=2)
        datafeed = BackDatafeed(symbol, start_date, timeframe, end_date, dataflux,
                                candles_extractor=CCXTCandlesExtractor())
        sizer = Sizer(bt.sizers.PercentSizer, percents=90)
        metrics = EngineMetricsCollection(TotalGrossProfit)
        assembly = ComponentsAssembly(broker, strategy, datafeed, sizer, metrics)
        engine = Engine(assembly)
        simulator = WalkForwardSimulator(periods=2, anchored=True)
        result = simulator.simulate(engine)


if __name__ == '__main__':
    unittest.main()
