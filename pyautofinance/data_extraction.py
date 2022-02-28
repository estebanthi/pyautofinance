import datetime as dt

from pyautofinance.common.feeds.extractors import CandlesExtractorsFactory
from pyautofinance.common.feeds.writers import CSVCandlesWriter
from pyautofinance.common.feeds.FeedTitle import FeedTitle
from pyautofinance.common.options import TimeOptions, MarketOptions, FeedOptions, Market
from pyautofinance.common.timeframes import h1

symbols = 'BTC-USD ETH-USD BNB-EUR ETH-BTC DOGE-BTC BNB-BTC AVAX-BTC BTC-USDT BTC-USD LTC-USD'.split(' ')

start_date = dt.datetime(2020, 1, 1)
end_date = dt.datetime(2022, 1, 1)
timeframe = h1()
time_options = TimeOptions(start_date, timeframe, end_date)

market_options = MarketOptions(Market.CRYPTO, symbols[0])

feed_options = FeedOptions(market_options, time_options)

extractors_factory = CandlesExtractorsFactory()
writer = CSVCandlesWriter()

for symbol in symbols:
    feed_options.market_options.symbol = symbol
    feed_title = FeedTitle(feed_options).get_pathname()

    feed = extractors_factory.get_candles(feed_options)
    writer.write(feed, feed_title)
