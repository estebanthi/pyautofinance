import datetime as dt
import warnings
warnings.filterwarnings('ignore')

from pyautofinance.common.timeframes import h1
from pyautofinance.common.dataflux import DiskDataflux
from pyautofinance.common.feeds.extractors import CCXTCandlesExtractor
from pyautofinance.common.feeds import BackDatafeed


def run(symbol, start_date, end_date, timeframe, dataflux, extractor):
    feed = BackDatafeed(symbol, start_date, timeframe, end_date, dataflux, candles_extractor=extractor)
    feed.extract()

if __name__ == '__main__':
    symbol = 'BTC-EUR'
    start_date = dt.datetime(2019, 1, 1)
    end_date = dt.datetime(2022, 3, 15)
    timeframe = h1
    dataflux = DiskDataflux()
    extractor = CCXTCandlesExtractor()

    run(symbol, start_date, end_date, timeframe, dataflux, extractor)
