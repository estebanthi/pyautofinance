from pyautofinance.common.feeds.filterers.candles_filterer import CandlesFilterer


class SimpleCandlesFilterer(CandlesFilterer):

    def __init__(self, start_date, end_date):
        self._start_date = start_date
        self._end_date = end_date

    def filter_candles(self, candles):
        self._filter_date_column(candles)
        return candles

    def _filter_date_column(self, candles):
        before_start_date = candles["Date"] < self._start_date
        candles.drop(candles.loc[before_start_date].index, inplace=True)

        after_end_date = candles["Date"] > self._end_date
        candles.drop(candles.loc[after_end_date].index, inplace=True)

        return candles.copy()
