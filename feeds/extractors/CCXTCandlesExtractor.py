from ccxt import bitfinex, binance
import datetime as dt
import pandas as pd
from feeds.extractors.CandlesExtractor import CandlesExtractor


class CCXTCandlesExtractor(CandlesExtractor):

    def _extract_candles(self, feed_options):
        market_options = feed_options.market_options
        time_options = feed_options.time_options

        exchange = self._get_exchange_from_market_options(market_options)
        symbol = self._get_symbol_from_market_options(market_options)
        timeframe = self._get_timeframe_from_time_options(time_options)
        since = self._get_since_from_time_options(time_options)

        first_10_000_candles = exchange.fetch_ohlcv(
            symbol=symbol,
            timeframe=timeframe,
            since=since,
            limit=10000
        )

        all_candles = self._bypass_candles_limit(first_10_000_candles, feed_options)
        df_candles = self._put_candles_in_dohlcv_df(all_candles)
        return df_candles

    def _bypass_candles_limit(self, source_candles, feed_options):
        while source_candles[-1][0] < dt.datetime.timestamp(
                feed_options.time_options.end_date) * 1000:  # If more than 10 000 candles

            market_options = feed_options.market_options
            time_options = feed_options.time_options

            exchange = self._get_exchange_from_market_options(market_options)
            symbol = self._get_symbol_from_market_options(market_options)
            timeframe = self._get_timeframe_from_time_options(time_options)

            # Extraction of the 10 000 next candles
            candles_to_add = exchange.fetch_ohlcv(
                symbol=symbol,
                timeframe=timeframe,
                since=source_candles[-1][0],
                limit=10000
            )

            self._merge_candles(source_candles, candles_to_add)

        return source_candles

    def _get_exchange_from_market_options(self, market_options):
        symbol = market_options.symbol
        return binance() if "BNB" in symbol else bitfinex()

    def _get_symbol_from_market_options(self, market_options):
        symbol = market_options.symbol
        formatted_symbol = self._format_symbol_for_ccxt(symbol)
        return formatted_symbol

    def _get_timeframe_from_time_options(self, time_options):
        timeframe = time_options.timeframe
        formatted_timeframe = self._format_timeframe_for_ccxt(timeframe)
        return formatted_timeframe

    def _get_since_from_time_options(self, time_options):
        start_date = time_options.start_date
        since = int(dt.datetime.timestamp(start_date) * 1000)
        return since

    def _put_candles_in_dohlcv_df(self, candles):
        columns = 'Date Open High Low Close Volume'.split(
            ' ')

        dataframe_candles = pd.DataFrame(candles, columns=columns)
        float_dataframe_candles = dataframe_candles.astype('float64')

        float_dataframe_candles.loc[:, "Date"] = float_dataframe_candles.loc[:, "Date"].apply(self._epoch_to_datetime)

        return float_dataframe_candles

    @staticmethod
    def _merge_candles(source_candles, candles_to_add):
        for i in range(len(candles_to_add)):
            if i != 0:
                source_candles.append(candles_to_add[i])

    @staticmethod
    def _epoch_to_datetime(epoch):
        epoch /= 1000
        return dt.datetime.fromtimestamp(epoch)

    @staticmethod
    def _format_symbol_for_ccxt(symbol):
        return symbol.replace("-", "/")

    @staticmethod
    def _format_timeframe_for_ccxt(timeframe):
        # We need to invert compression and unit to have a formatted timeframe
        formatted_timeframe = timeframe.value[::-1]
        return formatted_timeframe
