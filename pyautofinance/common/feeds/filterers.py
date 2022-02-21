import pandas as pd

from abc import ABC, abstractmethod

from pyautofinance.common.options import FeedOptions


class CandlesFilterer(ABC):

    @abstractmethod
    def filter_candles(self, candles: pd.DataFrame, feed_options: FeedOptions) -> pd.DataFrame:
        pass

    def _filter_date_column(self, candles, feed_options):
        pass

    def _filter_prices_columns(self, candles, feed_options):
        pass

    def _filter_volume_column(self, candles, feed_options):
        pass


class SimpleCandlesFilterer(CandlesFilterer):

    def filter_candles(self, candles: pd.DataFrame, feed_options):
        self._filter_date_column(candles, feed_options)
        self._filter_prices_columns(candles, feed_options)
        self._filter_volume_column(candles, feed_options)
        return candles

    @staticmethod
    def _filter_date_column(candles, feed_options):
        time_options = feed_options.time_options
        start_date = time_options.start_date
        end_date = time_options.end_date

        before_start_date = candles["Date"] < start_date
        candles.drop(candles.loc[before_start_date].index, inplace=True)

        after_end_date = candles["Date"] > end_date
        candles.drop(candles.loc[after_end_date].index, inplace=True)

        return candles.copy()
