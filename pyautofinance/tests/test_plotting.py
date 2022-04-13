import unittest
import datetime as dt

import backtrader as bt

from pyautofinance.common.engine import Engine, ComponentsAssembly
from pyautofinance.common.feeds import BackDatafeed
from pyautofinance.common.feeds.extractors import CCXTCandlesExtractor
from pyautofinance.common.dataflux import DiskDataflux
from pyautofinance.common.brokers import BackBroker
from pyautofinance.common.sizers import Sizer
from pyautofinance.common.metrics.engine_metrics import EngineMetricsCollection, TotalGrossProfit, TotalNetProfit
from pyautofinance.common.strategies import BracketStrategyExample, Strategy
from pyautofinance.common.timeframes import h4
from pyautofinance.common.results.strat_result import StratResult
from pyautofinance.common.plotting import BackPlotter
from pyautofinance.common.observers import Observer, AverageGainPerTrade


class TestPlotting(unittest.TestCase):

    start_date = dt.datetime(2020, 1, 1)
    end_date = dt.datetime(2021, 1, 1)
    symbol = 'BTC-EUR'
    timeframe = h4

    cash = 100000
    commission = 0.02

    dataflux = DiskDataflux()

    broker = BackBroker(cash, commission)
    strategy = Strategy(BracketStrategyExample, stop_loss=1, risk_reward=2)
    datafeed = BackDatafeed(symbol, start_date, timeframe, end_date, dataflux, candles_extractor=CCXTCandlesExtractor())
    sizer = Sizer(bt.sizers.PercentSizer, percents=10)
    metrics = EngineMetricsCollection(TotalGrossProfit, TotalNetProfit)
    observer = Observer(AverageGainPerTrade, average_gain=200, standard_deviation=300, X=2)

    assembly = ComponentsAssembly(broker, strategy, datafeed, sizer, metrics, BackPlotter(), observer)

    def test_simple_plotting(self):
        engine = Engine(self.assembly, optimized=False)
        engine.run()


if __name__ == '__main__':
    unittest.main()
