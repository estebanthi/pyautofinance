import datetime as dt
import backtrader as bt

from pyautofinance.common.options import FeedOptions, TimeOptions, MarketOptions, TimeFrame, Market

from pyautofinance.common.feeds.extractors import CSVCandlesExtractor, CCXTCandlesExtractor
from pyautofinance.common.feeds.datafeeds_generators import BacktestingDatafeedGenerator

from pyautofinance.common.feeds.writers import CandlesWriter
from pyautofinance.common.feeds.FeedTitle import FeedTitle

from pyautofinance.common.strategies.TestStrategy import TestStrategy


time_options = TimeOptions(dt.datetime(2020, 1, 1), dt.datetime(2022, 1, 1), TimeFrame.d1)
market_options = MarketOptions(Market.CRYPTO, "BTC-EUR")
feed_options = FeedOptions(market_options, time_options)

csv_extractor = CSVCandlesExtractor()
ccxt_extractor = CCXTCandlesExtractor()
candles = csv_extractor.get_formatted_and_filtered_candles(feed_options)

writer = CandlesWriter()
# writer.write(candles, FeedTitle(feed_options).get_pathname())

datafeed_generator = BacktestingDatafeedGenerator()
datafeed = datafeed_generator.generate_datafeed(candles, feed_options)

strategy = TestStrategy

cerebro = bt.Cerebro()
cerebro.broker.set_cash(1000000)
cerebro.adddata(datafeed)
cerebro.addstrategy(strategy, logging=True, stop_loss=10, risk_reward=2)
cerebro.run()