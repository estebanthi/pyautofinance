import datetime as dt
import warnings
warnings.filterwarnings('ignore')

import backtrader as bt

from pyautofinance.common.learn import TaLibPredicter
from pyautofinance.common.timeframes import h1
from pyautofinance.common.dataflux import DiskDataflux
from pyautofinance.common.feeds.extractors import CCXTCandlesExtractor
from pyautofinance.common.feeds import BackDatafeed
from pyautofinance.common.engine import Engine, ComponentsAssembly
from pyautofinance.common.brokers import BackBroker
from pyautofinance.common.strategies import Strategy, PredictingStrat
from pyautofinance.common.sizers import Sizer
from pyautofinance.common.metrics.engine_metrics import EngineMetricsCollection, TotalNetProfit


def run(broker, strategy, datafeed, sizer, metrics_collection):
    assembly = ComponentsAssembly(broker, strategy, datafeed, sizer, metrics_collection)
    engine = Engine(assembly)
    result = engine.run()
    for strat in result:
        print(strat.metrics)


if __name__ == '__main__':

    cash = 100_000
    commission = 0.001
    broker = BackBroker(cash, commission)

    predicter = TaLibPredicter('BTC-EUR 1h')
    strategy = Strategy(PredictingStrat, update_predicter=False, predicter=predicter, logging=True, train_period=340,
                        stop_loss=2, risk_reward=3)

    symbol = 'BTC-EUR'
    start_date = dt.datetime(2022, 3, 1)
    end_date = dt.datetime(2022, 4, 14)
    timeframe = h1
    dataflux = DiskDataflux()
    extractor = CCXTCandlesExtractor()
    datafeed = BackDatafeed(symbol, start_date, timeframe, end_date, dataflux, candles_extractor=extractor)

    sizer = Sizer(bt.sizers.PercentSizer, percents=10)

    metrics_collection = EngineMetricsCollection(TotalNetProfit)

    run(broker, strategy, datafeed, sizer, metrics_collection)
