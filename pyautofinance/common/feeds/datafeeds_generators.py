import time
import ccxt

from backtrader.feeds import PandasData
from abc import ABC, abstractmethod
from ccxtbt import CCXTStore

from pyautofinance.common.options import TimeFrame
from pyautofinance.common.config import Config


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

    def generate_datafeed(self, feed_options, exchange_options):
        exchange = exchange_options.exchange

        api_key = self._load_api_key(exchange)
        api_secret = self._load_api_secret(exchange)
        broker_config = {
            'apiKey': api_key,
            'secret': api_secret,
            'nonce': lambda: str(int(time.time() * 1000)),
            'enableRateLimit': True,
        }

        currency = exchange_options.currency
        store = CCXTStore(exchange=exchange.id, currency=currency, config=broker_config, retries=5,
                          debug=False)

        market_options = feed_options.market_options
        time_options = feed_options.time_options

        symbol = market_options.symbol
        formatted_symbol = self._format_symbol_for_ccxt(symbol)

        timeframe = time_options.timeframe
        bt_timeframe, bt_compression = TimeFrame.get_bt_timeframe_and_compression_from_timeframe(timeframe)

        start_date = time_options.start_date

        return store.getdata(dataname=formatted_symbol, name=formatted_symbol, timeframe=bt_timeframe,
                             fromdate=start_date, compression=bt_compression, ohlcv_limit=99999,
                             sessionstart=start_date)

    @staticmethod
    def _load_api_key(exchange):
        api_key_field_name = f"{exchange.id}_api_key"
        config = Config()
        return config.get_field(api_key_field_name)

    @staticmethod
    def _load_api_secret(exchange):
        api_secret_field_name = f"{exchange.id}_api_secret"
        config = Config()
        return config.get_field(api_secret_field_name)

    @staticmethod
    def _format_symbol_for_ccxt(symbol):
        return symbol.replace("-", "/")