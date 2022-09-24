import datetime as dt
import numpy as np
import warnings
warnings.filterwarnings('ignore')

import backtrader as bt

from pyautofinance.common.learn import TaLibPredicter
from pyautofinance.common.timeframes import h1, h4, m5, d1
from pyautofinance.common.dataflux import DiskDataflux
from pyautofinance.common.feeds.extractors import CCXTCandlesExtractor
from pyautofinance.common.feeds import BackDatafeed
from pyautofinance.common.engine import Engine, ComponentsAssembly
from pyautofinance.common.brokers import BackBroker
from pyautofinance.common.strategies import Strategy, EMAStopLoss
from pyautofinance.common.sizers import Sizer
from pyautofinance.common.metrics.engine_metrics import EngineMetricsCollection, TotalNetProfit, TotalGrossProfit
from pyautofinance.common.strategies.usable_strategies.generated_strat_1 import GeneratedStrategy1
from pyautofinance.common.strategies.usable_strategies.ema_crossovers import EMACrossOvers
from pyautofinance.common.strategies.usable_strategies.private_strategies.bbands_strat import BBandsStrat
from pyautofinance.common.strategies.usable_strategies.private_strategies.guppy_strat import GuppyStrat
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Tradimo


def run(broker, strategy, datafeed, sizer, metrics_collection):
    assembly = ComponentsAssembly(broker, strategy, datafeed, sizer, metrics_collection)
    engine = Engine(assembly, optimized=False)
    result = engine.run()

    best_net_profit_strat = result.sort_by_metric('TotalNetProfit')[0]
    best_net_profit = best_net_profit_strat['TotalNetProfit']
    best_params = best_net_profit_strat.params
    print(f'Best net profit: {best_net_profit}, best params: {best_params}')
    engine.plot(Bokeh(style='bar', plot_mode='single', scheme=Tradimo()))


if __name__ == '__main__':

    cash = 100_000
    commission = 0.001
    broker = BackBroker(cash, commission)

    strategy = Strategy(GuppyStrat, logging=False, stop_loss=1, risk_reward=2)

    symbol = 'ETH-EUR'
    start_date = dt.datetime(2020, 2, 1)
    end_date = dt.datetime(2022, 7, 19)
    timeframe = h4
    dataflux = DiskDataflux()
    extractor = CCXTCandlesExtractor()
    datafeed = BackDatafeed(symbol, start_date, timeframe, end_date, dataflux, candles_extractor=extractor)

    sizer = Sizer(bt.sizers.PercentSizer, percents=99)

    metrics_collection = EngineMetricsCollection(TotalNetProfit, TotalGrossProfit)

    run(broker, strategy, datafeed, sizer, metrics_collection)
