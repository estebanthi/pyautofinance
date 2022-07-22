import unittest
from unittest.mock import patch, MagicMock, create_autospec

import datetime as dt
import numpy as np
import warnings
import statistics
import time

warnings.filterwarnings('ignore')

import backtrader as bt

from pyautofinance.common.learn import TaLibPredicter
from pyautofinance.common.timeframes import h1, h4, m5, d1
from pyautofinance.common.dataflux import DiskDataflux
from pyautofinance.common.feeds.extractors import CCXTCandlesExtractor
from pyautofinance.common.feeds import BackDatafeed
from pyautofinance.common.engine import Engine, ComponentsAssembly
from pyautofinance.common.brokers import BackBroker
from pyautofinance.common.strategies.generated_strategy import GeneratedStrategy
from pyautofinance.common.sizers import Sizer
from pyautofinance.common.metrics.engine_metrics import EngineMetricsCollection, TotalNetProfit, TotalGrossProfit
from pyautofinance.common.strategies.generator.conditions_generator import ConditionsGenerator
from pyautofinance.common.strategies.generator.lines.ema_line import EMALine
from pyautofinance.common.strategies.generator.lines.close_line import CloseLine
from pyautofinance.common.collections.base_collection import BaseCollection
from pyautofinance.common.strategies.strategy import Strategy
from pyautofinance.common.strategies.generator.storage import Storage
from pyautofinance.common.strategies.generator.lines.bollinger_midband_line import BollingerMidBandLine
from pyautofinance.common.strategies.generator.lines.bollinger_botband_line import BollingerBotBandLine
from pyautofinance.common.strategies.generator.lines.bollinger_topband_line import BollingerTopBandLine
from pyautofinance.common.strategies.generator.lines.rsi_line import RSILine


cash = 100_000
commission = 0.001
broker = BackBroker(cash, commission)
symbol = 'BTC-EUR'
currency = 'EUR'
start_date = dt.datetime(2020, 2, 1)
end_date = dt.datetime(2022, 7, 19)
timeframe = d1
dataflux = DiskDataflux()
extractor = CCXTCandlesExtractor()
datafeed = BackDatafeed(symbol, start_date, timeframe, end_date, dataflux, candles_extractor=extractor)
sizer = Sizer(bt.sizers.PercentSizer, percents=99)
metrics_collection = EngineMetricsCollection(TotalNetProfit, TotalGrossProfit)


def generate_strat():
    conditions_generator = ConditionsGenerator()

    lines_to_use = BaseCollection([EMALine, CloseLine, BollingerMidBandLine, BollingerBotBandLine, BollingerTopBandLine,
                                   RSILine])

    open_long_conditions = conditions_generator.generate_conditions(lines_to_use, 1)
    open_long_conditions_storage = Storage(open_long_conditions)
    open_long_operators = conditions_generator.generate_operators(open_long_conditions)
    open_long_operators_storage = Storage(open_long_operators)

    open_short_conditions = conditions_generator.generate_conditions(lines_to_use, 2)
    open_short_conditions_storage = Storage(open_short_conditions)
    open_short_operators = conditions_generator.generate_operators(open_short_conditions)
    open_short_operators_storage = Storage(open_short_operators)

    close_long_conditions = conditions_generator.generate_conditions(lines_to_use, 1)
    close_long_conditions_storage = Storage(close_long_conditions)
    close_long_operators = conditions_generator.generate_operators(close_long_conditions)
    close_long_operators_storage = Storage(close_long_operators)

    close_short_conditions = conditions_generator.generate_conditions(lines_to_use, 1)
    close_short_conditions_storage = Storage(close_short_conditions)
    close_short_operators = conditions_generator.generate_operators(close_short_conditions)
    close_short_operators_storage = Storage(close_short_operators)

    indicators = Storage(
        conditions_generator.get_indicators(open_long_conditions) + conditions_generator.get_indicators(
            open_short_conditions) + conditions_generator.get_indicators(
            close_long_conditions) + conditions_generator.get_indicators(close_short_conditions))
    strategy = Strategy(GeneratedStrategy, open_long_conditions=open_long_conditions_storage,
                        open_long_operators=open_long_operators_storage,
                        open_short_conditions=open_short_conditions_storage,
                        open_short_operators=open_short_operators_storage,
                        close_long_conditions=close_long_conditions_storage,
                        close_long_operators=close_long_operators_storage,
                        close_short_conditions=close_short_conditions_storage,
                        close_short_operators=close_short_operators_storage, indicators_storage=indicators)
    return strategy, open_long_conditions, open_long_operators, open_short_conditions, open_short_operators, \
              close_long_conditions, close_long_operators, close_short_conditions, close_short_operators


iterations = 100
total_results = []
strategies = []
start_time = time.time()
for i in range(iterations):
    strategy, open_long_conditions, open_long_operators, open_short_conditions, open_short_operators, \
    close_long_conditions, close_long_operators, close_short_conditions, close_short_operators = generate_strat()
    assembly = ComponentsAssembly(broker, strategy, datafeed, sizer, metrics_collection)
    engine = Engine(assembly)
    result = engine.run()


    for strat in result:
        print(f"Iteration {i} out of {iterations} | Progress: {i / iterations * 100}%")
        total_results.append(strat.metrics['TotalNetProfit'].value)
        strategies.append({"Open long": (open_long_conditions, open_long_operators), "Open short": (open_short_conditions, open_short_operators),
                           "Close long": (close_long_conditions, close_long_operators), "Close short": (close_short_conditions, close_short_operators)})


print(f"Ran {iterations} strategies for {symbol} from {start_date} to {end_date} with {cash} {currency}\n")
print(f"Average profit : {statistics.mean(total_results)} {currency}")
print(f"Std : {statistics.stdev(total_results)} {currency}")
print(f"Median profit : {statistics.median(total_results)} {currency}")
print(f"Min profit : {min(total_results)} {currency}")
print(f"Max profit : {max(total_results)} {currency}")

max_index = total_results.index(max(total_results))

end_time = time.time()
print(f"\nTime elapsed: {round(end_time - start_time, 2)}s")
print(f"Best conditions found : {strategies[max_index]}")