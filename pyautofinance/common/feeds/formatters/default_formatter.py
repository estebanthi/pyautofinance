from pyautofinance.common.feeds.formatters.candles_formatter import CandlesFormatter


class DefaultCandlesFormatter(CandlesFormatter):

    def format_candles(self, candles):
        candles = self._format_date_column(candles)
        return candles
