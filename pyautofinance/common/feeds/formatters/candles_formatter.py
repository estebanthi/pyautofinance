import pandas as pd

from abc import ABC, abstractmethod


class CandlesFormatter(ABC):

    @abstractmethod
    def format_candles(self, candles: pd.DataFrame) -> pd.DataFrame:
        pass

    def _format_date_column(self, candles):
        pass

    def _format_prices_columns(self, candles):
        pass

    def _format_volume_column(self, candles):
        pass
