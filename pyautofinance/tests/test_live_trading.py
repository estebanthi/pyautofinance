import unittest
import datetime as dt

import backtrader as bt
import ccxt

from pyautofinance.common.engine import Engine, ComponentsAssembly
from pyautofinance.common.feeds import CCXTDatafeed
from pyautofinance.common.dataflux import DiskDataflux
from pyautofinance.common.brokers import BackBroker
from pyautofinance.common.sizers import Sizer
from pyautofinance.common.metrics.engine_metrics import EngineMetricsCollection, TotalGrossProfit
from pyautofinance.common.strategies import BracketStrategyExample, Strategy
from pyautofinance.common.strategies.usable_strategies.live_trading_test_strategy import LiveTradingTestStrategy
from pyautofinance.common.timeframes import m1
from pyautofinance.common.metrics.live_metrics import ActualProfit, LiveMetricsCollection


class TestEngine(unittest.TestCase):

    start_date = dt.datetime.now() - dt.timedelta(hours=2, minutes=1)
    symbol = 'BNB-BTC'
    timeframe = m1
    exchange = ccxt.binance()
    currency = 'BTC'

    cash = 100000
    commission = 0.02

    dataflux = DiskDataflux()

    broker = BackBroker(cash, commission)

    live_metrics = LiveMetricsCollection(ActualProfit)
    strategy = Strategy(LiveTradingTestStrategy, logging=True, stop_loss=0.5, risk_reward=2, live=True,
                        live_metrics=live_metrics, live_writing_interval=dt.timedelta(minutes=5))

    datafeed = CCXTDatafeed(symbol, start_date, timeframe, exchange, currency)
    sizer = Sizer(bt.sizers.PercentSizer, percents=10)
    metrics = EngineMetricsCollection()

    assembly = ComponentsAssembly(broker, strategy, datafeed, sizer, metrics, dataflux)

    def test_run(self):
        engine = Engine(self.assembly)
        engine.run()


if __name__ == '__main__':
    unittest.main()
