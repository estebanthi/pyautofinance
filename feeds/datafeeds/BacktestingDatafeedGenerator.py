from backtrader.feeds import PandasData
from feeds.datafeeds.DatafeedGenerator import DatafeedGenerator
from enums.TimeFrame import TimeFrame


class BacktestingDatafeedGenerator(DatafeedGenerator):

    def generate_datafeed(self, candles, feed_options):
        time_options = feed_options.time_options
        timeframe = time_options.timeframe

        bt_timeframe, compression = TimeFrame.get_bt_timeframe_and_compression_from_timeframe(timeframe)

        return PandasData(dataname=candles, timeframe=timeframe, compression=compression)
