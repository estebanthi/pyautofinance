import datetime as dt
import warnings
warnings.filterwarnings('ignore')

import pandas_ta as ta
from sklearn.ensemble import RandomForestClassifier

from pyautofinance.common.timeframes import h1
from pyautofinance.common.dataflux import DiskDataflux
from pyautofinance.common.feeds.extractors import CCXTCandlesExtractor
from pyautofinance.common.feeds import BackDatafeed
from pyautofinance.common.learn import TaLibPredicter


def run(symbol, start_date, end_date, timeframe, dataflux, predicter, extractor=None):
    feed = BackDatafeed(symbol, start_date, timeframe, end_date, dataflux, candles_extractor=extractor)

    predicter.fit(feed)
    predicter.save('BTC-EUR 1h')

if __name__ == '__main__':
    symbol = 'BTC-EUR'
    start_date = dt.datetime(2019, 1, 1)
    end_date = dt.datetime(2022, 3, 15)
    timeframe = h1
    dataflux = DiskDataflux()
    extractor = CCXTCandlesExtractor()

    model = RandomForestClassifier()
    strategy = ta.AllStrategy
    predicter = TaLibPredicter(model=model, ta_strategy=strategy)

    run(symbol, start_date, end_date, timeframe, dataflux, predicter, extractor=extractor)
