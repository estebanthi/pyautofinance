import pandas as pd
import datetime as dt

from abc import ABC, abstractmethod


class CandlesFormatter(ABC):

    @abstractmethod
    def format_candles(self, candles: pd.DataFrame) -> pd.DataFrame:
        pass

    def _format_date_column(self, candles):
        candles['Date'] = pd.to_datetime(candles['Date'], format='%Y-%m-%d %H:%M:%S')
        return candles

    def _format_prices_columns(self, candles):
        pass

    def _format_volume_column(self, candles):
        pass
