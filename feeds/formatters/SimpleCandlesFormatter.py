from feeds.formatters.CandlesFormatter import CandlesFormatter
import pandas as pd


class SimpleCandlesFormatter(CandlesFormatter):

    def format_candles(self, candles, feed_options):
        self._format_date_column(candles, feed_options)
        self._format_prices_columns(candles, feed_options)
        self._format_volume_column(candles, feed_options)
        return candles

    @staticmethod
    def _format_date_column(candles, feed_options):
        candles["Date"] = pd.to_datetime(candles["Date"])
        return candles
