from backtrader.feeds import PandasData
from abc import ABC, abstractmethod

from pyautofinance.common.options import TimeFrame, DateFormat


class DatafeedGenerator(ABC):

    @abstractmethod
    def generate_datafeed(self):
        pass


class BacktestingDatafeedGenerator(DatafeedGenerator):

    def generate_datafeed(self, candles, feed_options):
        time_options = feed_options.time_options
        timeframe = time_options.timeframe

        bt_timeframe, compression = TimeFrame.get_bt_timeframe_and_compression_from_timeframe(timeframe)

        return PandasData(dataname=candles, timeframe=bt_timeframe, compression=compression, datetime=0)
