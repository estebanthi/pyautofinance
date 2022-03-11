from pyautofinance.common.feeds.filterers.candles_filterer import CandlesFilterer


class DefaultCandlesFilterer(CandlesFilterer):

    def filter_candles(self, candles):
        return candles
