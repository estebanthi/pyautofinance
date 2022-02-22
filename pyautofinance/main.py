import datetime as dt
import backtrader as bt
import ccxt

from pyautofinance.common.options import FeedOptions, TimeOptions, MarketOptions, BrokerOptions, TimeFrame, Market

from pyautofinance.common.feeds.extractors import CSVCandlesExtractor, CCXTCandlesExtractor
from pyautofinance.common.feeds.datafeeds_generators import BacktestingDatafeedGenerator, CryptoLiveDatafeedGenerator

from pyautofinance.common.feeds.writers import CandlesWriter
from pyautofinance.common.feeds.FeedTitle import FeedTitle

from pyautofinance.common.strategies.bracket_strategies import TestStrategy
from pyautofinance.common.strategies.StrategiesFactory import StrategiesFactory


time_options = TimeOptions(dt.datetime(2020, 1, 1), end_date=dt.datetime(2022, 1, 1), timeframe=TimeFrame.d1)
market_options = MarketOptions(Market.CRYPTO, "BTC-EUR")
feed_options = FeedOptions(market_options, time_options)

csv_extractor = CSVCandlesExtractor()
ccxt_extractor = CCXTCandlesExtractor()
candles = csv_extractor.get_formatted_and_filtered_candles(feed_options)

writer = CandlesWriter()
# writer.write(candles, FeedTitle(feed_options).get_pathname())

datafeed_generator = BacktestingDatafeedGenerator()
datafeed = datafeed_generator.generate_datafeed(candles, feed_options)

strategies_factory = StrategiesFactory

strategy = strategies_factory.make_strategy(TestStrategy, logging=False, stop_loss=10, risk_reward=2)

cerebro = bt.Cerebro()
cerebro.broker.set_cash(1000000)
cerebro.adddata(datafeed)
cerebro.addstrategy(strategy[0], **strategy[1])
cerebro.run()

live_time_options = TimeOptions(dt.datetime(2022, 2, 22), end_date=dt.datetime(2023, 1, 1), timeframe=TimeFrame.m1)
broker_options = BrokerOptions(exchange=ccxt.binance(), currency="EUR")
live_feed_options = FeedOptions(market_options, live_time_options)

datafeed_generator = CryptoLiveDatafeedGenerator()
datafeed = datafeed_generator.generate_datafeed(live_feed_options, broker_options)
print(type(datafeed))
cerebro = bt.Cerebro()
cerebro.adddata(datafeed)
cerebro.addstrategy(strategy[0], **strategy[1])
cerebro.run()