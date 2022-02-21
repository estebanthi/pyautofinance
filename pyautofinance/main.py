import datetime as dt

from pyautofinance.common.options import FeedOptions, TimeOptions, MarketOptions, TimeFrame, Market

from pyautofinance.common.feeds.extractors import CCXTCandlesExtractor
from pyautofinance.common.feeds.writers import CandlesWriter

from pyautofinance.common.feeds.FeedTitle import FeedTitle


time_options = TimeOptions(dt.datetime(2020, 1, 1), dt.datetime(2020, 3, 1), TimeFrame.d1)
market_options = MarketOptions(Market.CRYPTO, "BTC-EUR")
feed_options = FeedOptions(market_options, time_options)

extractor = CCXTCandlesExtractor()
candles = extractor.get_formatted_and_filtered_candles(feed_options)

candles_pathname = FeedTitle(feed_options).get_pathname()

writer = CandlesWriter()
writer.write(candles, candles_pathname)
