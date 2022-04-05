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
from pyautofinance.common.strategies import Strategy
from pyautofinance.common.strategies.test_strats.monkey_strat import MonkeyStrat
from pyautofinance.common.timeframes import h4
from pyautofinance.common.simulators import MonkeySimulator


class TestMonkeySimulator(unittest.TestCase):

    start_date = dt.datetime(2020, 1, 1)
    end_date = dt.datetime(2022, 1, 1)
    symbol = 'BTC-EUR'
    timeframe = h4

    cash = 100000
    commission = 0.02

    dataflux = DiskDataflux()

    broker = BackBroker(cash, commission)
    monkey_full = Strategy(MonkeyStrat, entries_proba=0.1, exits_proba=0.1)
    datafeed = BackDatafeed(symbol, start_date, timeframe, end_date, dataflux, candles_extractor=CCXTCandlesExtractor())
    sizer = Sizer(bt.sizers.PercentSizer, percents=10)
    metrics = EngineMetricsCollection(TotalGrossProfit)

    assembly = ComponentsAssembly(broker, monkey_full, datafeed, sizer, metrics, dataflux)

    def test_simulate(self):
        engine = Engine(self.assembly)
        simulator = MonkeySimulator(iterations=2, monkey_full=self.monkey_full)
        result = simulator.simulate(engine)
        result['full'].get_average_metric('TotalGrossProfit')


if __name__ == '__main__':
    unittest.main()
