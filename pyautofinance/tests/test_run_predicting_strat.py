import unittest
import datetime as dt
import warnings
warnings.filterwarnings('ignore')

from sklearn.ensemble import RandomForestClassifier
import pandas_ta as ta
import backtrader as bt


from pyautofinance.common.engine import Engine, ComponentsAssembly
from pyautofinance.common.feeds import BackDatafeed
from pyautofinance.common.feeds.extractors import CCXTCandlesExtractor
from pyautofinance.common.dataflux import DiskDataflux
from pyautofinance.common.brokers import BackBroker
from pyautofinance.common.sizers import Sizer
from pyautofinance.common.metrics.engine_metrics import EngineMetricsCollection, TotalGrossProfit
from pyautofinance.common.strategies import BracketStrategyExample, Strategy, PredictingStrat
from pyautofinance.common.timeframes import h1
from pyautofinance.common.learn import TaLibPredicter


class TestRunPredictingStrat(unittest.TestCase):

    start_date = dt.datetime(2020, 1, 1)
    end_date = dt.datetime(2022, 3, 15)
    symbol = 'BTC-EUR'
    timeframe = h1

    cash = 100000
    commission = 0.02

    dataflux = DiskDataflux()

    broker = BackBroker(cash, commission)
    model = RandomForestClassifier()
    strategy = ta.AllStrategy
    predicter = TaLibPredicter(model=model, ta_strategy=strategy)
    strategy = Strategy(PredictingStrat, predicter=predicter, update_predicter=True, logging=True)
    datafeed = BackDatafeed(symbol, start_date, timeframe, end_date, dataflux, candles_extractor=CCXTCandlesExtractor())
    sizer = Sizer(bt.sizers.PercentSizer, percents=10)
    metrics = EngineMetricsCollection(TotalGrossProfit)

    assembly = ComponentsAssembly(broker, strategy, datafeed, sizer, metrics, dataflux)

    def test_run(self):
        engine = Engine(self.assembly)
        engine.run()


if __name__ == '__main__':
    unittest.main()
