from ccxt import bitfinex, binance
import datetime as dt
from feeds.extractors.CandlesExtractor import CandlesExtractor
import pandas as pd


class CCXTCandlesExtractor(CandlesExtractor):

    def _extract_candles(self, feed_options):
        market_options = feed_options.market_options
        time_options = feed_options.time_options

        exchange = self.get_exchange_from_market_options(market_options)
        symbol = self.get_symbol_from_market_options(market_options)
        timeframe = self.get_timeframe_from_time_options(time_options)
        since = self.get_since_from_time_options(time_options)

        limit_candles = exchange.fetch_ohlcv(
            symbol=symbol,
            timeframe=timeframe,
            since=since,
            limit=10000
        )

        all_candles = self.bypass_candles_limit(limit_candles, feed_options)
        formatted_candles = format_candles(all_candles)
        return formatted_candles

    def bypass_candles_limit(self, source_candles, feed_options):
        while source_candles[-1][0] < dt.datetime.timestamp(
                feed_options.time_options.end_date) * 1000:  # If more than 10 000 candles

            market_options = feed_options.market_options
            time_options = feed_options.time_options

            exchange = self.get_exchange_from_market_options(market_options)
            symbol = self.get_symbol_from_market_options(market_options)
            timeframe = self.get_timeframe_from_time_options(time_options)

            # Extraction of the 10 000 next candles
            candles_to_add = exchange.fetch_ohlcv(
                symbol=symbol,
                timeframe=timeframe,
                since=source_candles[-1][0],
                limit=10000
            )

            merge_candles(source_candles, candles_to_add)

        return source_candles

    @staticmethod
    def get_exchange_from_market_options(market_options):
        symbol = market_options.symbol
        return binance() if "BNB" in symbol else bitfinex()

    @staticmethod
    def get_symbol_from_market_options(market_options):
        symbol = market_options.symbol
        formatted_symbol = format_symbol_for_ccxt_exchange(symbol)
        return formatted_symbol

    @staticmethod
    def get_timeframe_from_time_options(time_options):
        timeframe = time_options.timeframe
        formatted_timeframe = format_timeframe_for_ccxt_exchange(timeframe)
        return formatted_timeframe

    @staticmethod
    def get_since_from_time_options(time_options):
        start_date = time_options.start_date
        since = int(dt.datetime.timestamp(start_date) * 1000)
        return since


def format_candles(candles):
    columns = 'Date Open High Low Close Volume'.split(
        ' ')

    dataframe_candles = pd.DataFrame(candles, columns=columns)
    float_dataframe_candles = dataframe_candles.astype('float64')

    float_dataframe_candles.loc[:, "Date"] = float_dataframe_candles.loc[:, "Date"].apply(epoch_to_datetime)

    return float_dataframe_candles


def merge_candles(source_candles, candles_to_add):
    for i in range(len(candles_to_add)):
        if i != 0:
            source_candles.append(candles_to_add[i])


def epoch_to_datetime(epoch):
    epoch /= 1000
    return dt.datetime.fromtimestamp(epoch)


def format_symbol_for_ccxt_exchange(symbol):
    return symbol.replace("-", "/")


def format_timeframe_for_ccxt_exchange(timeframe):
    # We need to invert compression and unit to have a formatted timeframe
    formatted_timeframe = timeframe.value[::-1]
    return formatted_timeframe
