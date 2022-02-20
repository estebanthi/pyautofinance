import pandas as pd
from abc import ABC, abstractmethod
from feeds.options.FeedOptions import FeedOptions


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
