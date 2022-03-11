import datetime as dt
import pandas as pd
import ccxt

from pyautofinance.common.feeds.extractors.candles_extractor import CandlesExtractor


class CCXTCandlesExtractor(CandlesExtractor):

    def extract_candles(self, ohlcv):
        symbol = ohlcv.symbol
        start_date = ohlcv.start_date
        end_date = ohlcv.end_date
        timeframe = ohlcv.timeframe

        exchange = self._get_exchange(symbol)
        symbol = self._get_symbol(symbol)
        since = self._get_since(start_date)

        first_10_000_candles = exchange.fetch_ohlcv(
            symbol=symbol,
            timeframe=timeframe.ccxt_name,
            since=since,
            limit=10000
        )

        all_candles = self._bypass_candles_limit(first_10_000_candles, symbol, timeframe, end_date)
        candles_dataframe = self._get_ohlcv_df_from_candles(all_candles)
        candles_dataframe = self._filter_candles_using_date(candles_dataframe, start_date, end_date)
        return candles_dataframe

    def _bypass_candles_limit(self, source_candles, symbol, timeframe, end_date):
        while source_candles[-1][0] < dt.datetime.timestamp(end_date) * 1000:  # If more than 10 000 candles

            exchange = self._get_exchange(symbol)
            symbol = self._get_symbol(symbol)

            # Extraction of the 10 000 next candles
            candles_to_add = exchange.fetch_ohlcv(
                symbol=symbol,
                timeframe=timeframe.ccxt_name,
                since=source_candles[-1][0],
                limit=10000
            )

            self._merge_candles(source_candles, candles_to_add)

        return source_candles

    @staticmethod
    def _get_exchange(symbol):
        return ccxt.binance() if "BNB" in symbol else ccxt.bitfinex()

    @staticmethod
    def _get_symbol(symbol):
        formatted_symbol = symbol.replace("-", "/")
        return formatted_symbol

    @staticmethod
    def _get_since(start_date):
        since = int(dt.datetime.timestamp(start_date) * 1000)
        return since

    def _get_ohlcv_df_from_candles(self, candles):
        columns = 'Date Open High Low Close Volume'.split(
            ' ')

        dataframe_candles = pd.DataFrame(candles, columns=columns)
        float_dataframe_candles = dataframe_candles.astype('float64')

        float_dataframe_candles.loc[:, "Date"] = float_dataframe_candles.loc[:, "Date"].apply(
            self._epoch_to_datetime)

        return float_dataframe_candles

    @staticmethod
    def _merge_candles(source_candles, candles_to_add):
        for i in range(len(candles_to_add)):
            if i != 0:
                source_candles.append(candles_to_add[i])
        return source_candles.copy()

    @staticmethod
    def _epoch_to_datetime(epoch):
        epoch /= 1000
        return dt.datetime.fromtimestamp(epoch)

    @staticmethod
    def _filter_candles_using_date(candles, start_date, end_date):
        before_start_date = candles["Date"] < start_date
        candles.drop(candles.loc[before_start_date].index, inplace=True)

        after_end_date = candles["Date"] > end_date
        candles.drop(candles.loc[after_end_date].index, inplace=True)

        return candles
