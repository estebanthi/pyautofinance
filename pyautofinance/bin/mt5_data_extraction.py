import datetime as dt
import warnings
warnings.filterwarnings('ignore')

from pyautofinance.common.timeframes import h1, h4
from pyautofinance.common.dataflux import DiskDataflux
from pyautofinance.common.feeds.extractors import CCXTCandlesExtractor
from pyautofinance.common.feeds.extractors.metatrader5_extractor import Metatrader5Extractor
from pyautofinance.common.feeds import BackDatafeed


def run(symbol, start_date, end_date, timeframe, dataflux, extractor):
    feed = BackDatafeed(symbol, start_date, timeframe, end_date, dataflux, candles_extractor=extractor)
    feed.extract()

if __name__ == '__main__':
    symbol = 'EUR-USD'
    start_date = dt.datetime(2010, 9, 27)
    end_date = dt.datetime(2022, 9, 23, 20, 0)
    timeframe = h4
    dataflux = DiskDataflux()
    extractor = Metatrader5Extractor()

    run(symbol, start_date, end_date, timeframe, dataflux, extractor)
