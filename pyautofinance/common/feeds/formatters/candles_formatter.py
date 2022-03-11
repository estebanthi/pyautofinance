import pandas as pd

from abc import ABC, abstractmethod


class CandlesFormatter(ABC):

    @abstractmethod
    def format_candles(self, candles: pd.DataFrame, feed_options) -> pd.DataFrame:
        pass

    def _format_date_column(self, candles, feed_options):
        pass

    def _format_prices_columns(self, candles, feed_options):
        pass

    def _format_volume_column(self, candles, feed_options):
        pass
