import time
import ccxt

from backtrader.feeds import PandasData
from abc import ABC, abstractmethod
from ccxtbt import CCXTStore

from pyautofinance.common.options import TimeFrame
from pyautofinance.common.feeds.extractors import CCXTCandlesExtractor
from pyautofinance.common.feeds.ccxt_utils import format_symbol_for_ccxt
from pyautofinance.common.broker.BrokerConfig import BrokerConfig


class DatafeedGenerator(ABC):

    @abstractmethod
    def generate_datafeed(self):
        pass


class BacktestingDatafeedGenerator(DatafeedGenerator):

    def generate_datafeed(self, candles, feed_options):
        time_options = feed_options.time_options
        timeframe = time_options.timeframe

        bt_timeframe, compression = TimeFrame.get_bt_timeframe_and_compression_from_timeframe(timeframe)

        return PandasData(dataname=candles, timeframe=bt_timeframe, compression=compression, datetime=0)


class CryptoLiveDatafeedGenerator(DatafeedGenerator):

    def generate_datafeed(self, feed_options, broker_options):
        exchange = broker_options.exchange

        broker_config = BrokerConfig(broker_options)

        currency = broker_options.currency
        store = CCXTStore(exchange=exchange.id, currency=currency, config=broker_config.get_live_config(), retries=5,
                          debug=False)

        market_options = feed_options.market_options
        time_options = feed_options.time_options

        symbol = market_options.symbol
        formatted_symbol = format_symbol_for_ccxt(symbol)

        timeframe = time_options.timeframe
        bt_timeframe, bt_compression = TimeFrame.get_bt_timeframe_and_compression_from_timeframe(timeframe)

        start_date = time_options.start_date

        return store.getdata(dataname=formatted_symbol, name=formatted_symbol, timeframe=bt_timeframe,
                             fromdate=start_date, compression=bt_compression, ohlcv_limit=99999,
                             sessionstart=start_date)
