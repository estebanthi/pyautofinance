import datetime as dt

from pyautofinance.common.timeframes import h1
from pyautofinance.common.dataflux import DiskDataflux
from pyautofinance.common.feeds.extractors import CCXTCandlesExtractor
from pyautofinance.common.feeds import BackDatafeed


symbol = 'BTC-EUR'
start_date = dt.datetime(2019, 1, 1)
end_date = dt.datetime(2022, 3, 15)
timeframe = h1
extractor = CCXTCandlesExtractor()
dataflux = DiskDataflux()

feed = BackDatafeed(symbol, start_date, timeframe, end_date, dataflux, candles_extractor=extractor)
feed.extract()
