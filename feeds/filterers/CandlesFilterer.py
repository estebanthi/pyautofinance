import pandas as pd
from abc import ABC, abstractmethod
from feeds.options.FeedOptions import FeedOptions


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
