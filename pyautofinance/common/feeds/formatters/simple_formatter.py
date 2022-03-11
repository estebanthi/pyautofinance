import pandas as pd
import math

from pyautofinance.common.feeds.formatters.candles_formatter import CandlesFormatter


class SimpleCandlesFormatter(CandlesFormatter):

    def __init__(self, numeric_decimals):
        self._numeric_decimals = numeric_decimals

    def format_candles(self, candles):
        self._format_date_column(candles)
        self._format_prices_columns(candles)
        return candles

    @staticmethod
    def _format_date_column(candles):
        candles["Date"] = pd.to_datetime(candles["Date"])

    @staticmethod
    def _format_volume_column(candles):
        candles["Volume"] = candles["Volume"].apply(lambda x: math.trunc(x*100)/100)
