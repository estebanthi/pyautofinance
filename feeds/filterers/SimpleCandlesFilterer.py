import pandas as pd
from feeds.filterers.CandlesFilterer import CandlesFilterer


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

        after = candles[candles["Date"] >= start_date]
        before = candles[candles["Date"] <= end_date]
        between = after.merge(before)

        return between

