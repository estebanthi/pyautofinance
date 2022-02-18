from backtrader.feeds import PandasData
from feeds.datafeeds.DatafeedGenerator import DatafeedGenerator


class BacktestingDatafeedGenerator(DatafeedGenerator):

    def generate_backtesting_datafeed(self, candles, feed_options):
        timeframe, compression = self.parse_timeframe(feed_options.time_options.timeframe)
        return PandasData(dataname=candles, timeframe=timeframe, compression=compression)
