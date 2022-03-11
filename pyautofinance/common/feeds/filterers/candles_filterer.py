import pandas as pd

from abc import ABC, abstractmethod


class CandlesFilterer(ABC):

    @abstractmethod
    def filter_candles(self, candles: pd.DataFrame) -> pd.DataFrame:
        pass

    def _filter_date_column(self, candles):
        pass

    def _filter_prices_columns(self, candles):
        pass

    def _filter_volume_column(self, candles):
        pass
