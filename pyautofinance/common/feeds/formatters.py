import pandas as pd
import math

from abc import ABC, abstractmethod

from pyautofinance.common.options import FeedOptions


class CandlesFormatter(ABC):

    @abstractmethod
    def format_candles(self, candles: pd.DataFrame, feed_options: FeedOptions) -> pd.DataFrame:
        pass

    def _format_date_column(self, candles, feed_options):
        pass

    def _format_prices_columns(self, candles, feed_options):
        pass

    def _format_volume_column(self, candles, feed_options):
        pass


class SimpleCandlesFormatter(CandlesFormatter):

    def format_candles(self, candles, feed_options):
        self._format_date_column(candles, feed_options)
        self._format_prices_columns(candles, feed_options)
        self._format_volume_column(candles, feed_options)
        return candles

    @staticmethod
    def _format_date_column(candles, feed_options):
        candles["Date"] = pd.to_datetime(candles["Date"])
        return candles.copy()

    @staticmethod
    def _format_volume_column(candles, feed_options):
        candles["Volume"] = candles["Volume"].apply(lambda x: math.trunc(x*100)/100)
