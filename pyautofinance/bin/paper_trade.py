import datetime as dt
import warnings
warnings.filterwarnings('ignore')

import backtrader as bt
import ccxt

from pyautofinance.common.learn import TaLibPredicter
from pyautofinance.common.timeframes import h1, h4, m5, d1, m1
from pyautofinance.common.dataflux import DiskDataflux
from pyautofinance.common.feeds.extractors import CCXTCandlesExtractor
from pyautofinance.common.feeds import CCXTDatafeed
from pyautofinance.common.engine import Engine, ComponentsAssembly
from pyautofinance.common.brokers import BackBroker
from pyautofinance.common.strategies import Strategy, EMAStopLoss
from pyautofinance.common.sizers import Sizer
from pyautofinance.common.metrics.engine_metrics import EngineMetricsCollection, TotalNetProfit, TotalGrossProfit


def run(broker, strategy, datafeed, sizer, metrics_collection):
    assembly = ComponentsAssembly(broker, strategy, datafeed, sizer, metrics_collection)
    engine = Engine(assembly)
    result = engine.run()
    for strat in result:
        print(strat.metrics)


if __name__ == '__main__':

    cash = 2_000
    commission = 0.001
    broker = BackBroker(cash, commission)

    strategy = Strategy(EMAStopLoss, logging=True, stop_loss=5, risk_reward=5)

    symbol = 'ETH-BTC'
    start_date = dt.datetime(2022, 7, 18)
    timeframe = m1
    dataflux = DiskDataflux()
    extractor = CCXTCandlesExtractor()
    datafeed = CCXTDatafeed(symbol, start_date, timeframe, ccxt.binance(), 'BTC', True)

    sizer = Sizer(bt.sizers.PercentSizer, percents=99)

    metrics_collection = EngineMetricsCollection(TotalNetProfit, TotalGrossProfit)

    run(broker, strategy, datafeed, sizer, metrics_collection)
