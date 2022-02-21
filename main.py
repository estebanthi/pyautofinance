import datetime as dt

from feeds.options.FeedOptions import FeedOptions
from feeds.options.TimeOptions import TimeOptions
from feeds.options.MarketOptions import MarketOptions

from enums.TimeFrame import TimeFrame
from enums.Market import Market

from feeds.extractors.CCXTCandlesExtractor import CCXTCandlesExtractor
from feeds.writers.CandlesWriter import CandlesWriter

from feeds.FeedTitle import FeedTitle


time_options = TimeOptions(dt.datetime(2020, 1, 1), dt.datetime(2020, 3, 1), TimeFrame.d1)
market_options = MarketOptions(Market.CRYPTO, "BTC-EUR")
feed_options = FeedOptions(market_options, time_options)

extractor = CCXTCandlesExtractor()
candles = extractor.get_formatted_and_filtered_candles(feed_options)

candles_pathname = FeedTitle(feed_options).get_pathname()

writer = CandlesWriter()
writer.write(candles, candles_pathname)
