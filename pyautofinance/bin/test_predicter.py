import datetime as dt
import warnings
warnings.filterwarnings('ignore')

from pyautofinance.common.learn import TaLibPredicter
from pyautofinance.common.testers import ClassificationTester
from pyautofinance.common.timeframes import h1
from pyautofinance.common.dataflux import DiskDataflux
from pyautofinance.common.feeds.extractors import CCXTCandlesExtractor
from pyautofinance.common.feeds import BackDatafeed
from pyautofinance.common.engine import Engine, ComponentsAssembly
from pyautofinance.common.brokers import BackBroker
from pyautofinance.common.strategies import Strategy
from pyautofinance.common.sizers import Sizer
from pyautofinance.common.metrics.engine_metrics import EngineMetricsCollection


def run(symbol, start_date, end_date, timeframe, dataflux, predicter, extractor=None):
    broker = BackBroker(100000, 0.001)
    strategy = Strategy(None)
    feed = BackDatafeed(symbol, start_date, timeframe, end_date, dataflux, candles_extractor=extractor)
    sizer = Sizer(None)
    metrics = EngineMetricsCollection()

    assembly = ComponentsAssembly(broker, strategy, feed, sizer, metrics)
    engine = Engine(assembly)

    tester = ClassificationTester(predicter)
    result = tester.test(engine)[0]
    print(result)

if __name__ == '__main__':
    symbol = 'BTC-EUR'
    start_date = dt.datetime(2022, 3, 15)
    end_date = dt.datetime(2022, 4, 14)
    timeframe = h1
    dataflux = DiskDataflux()
    extractor = CCXTCandlesExtractor()

    predicter = TaLibPredicter('BTC-EUR 1h')

    run(symbol, start_date, end_date, timeframe, dataflux, predicter, extractor=extractor)
