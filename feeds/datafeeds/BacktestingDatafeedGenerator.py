from backtrader.feeds import PandasData
from feeds.datafeeds.DatafeedGenerator import DatafeedGenerator
import pandas as pd


class BacktestingDatafeedGenerator(DatafeedGenerator):

    def generate_backtesting_datafeed(self, candles, feed_options):
        timeframe, compression = self.parse_timeframe(feed_options.time_options.timeframe)
        start_date = feed_options.time_options.start_date
        end_date = feed_options.time_options.end_date

        filtered_candles = filter_candles(start_date, end_date, candles)
        return PandasData(dataname=candles, timeframe=timeframe, compression=compression)


def filter_candles(start, end, candles):
    df = pd.DataFrame()
    df = df.from_records(candles)

    df["Date"] = pd.to_datetime(df["Date"])

    after = df[df["Date"] >= start]
    before = df[df["Date"] <= end]
    between = after.merge(before)

    return between
