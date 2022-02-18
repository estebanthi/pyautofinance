from enums import TimeFrame
import backtrader as bt


class DatafeedGenerator:

    timeframes_mapper = {
        's1': (bt.TimeFrame.Seconds, 1),
        'm1': (bt.TimeFrame.Minutes, 1),
        'm5': (bt.TimeFrame.Minutes, 5),
        'm15': (bt.TimeFrame.Minutes, 15),
        'm30': (bt.TimeFrame.Minutes, 30),
        'm45': (bt.TimeFrame.Minutes, 45),
        'h1': (bt.TimeFrame.Minutes, 60),
        'h2': (bt.TimeFrame.Minutes, 120),
        'h4': (bt.TimeFrame.Minutes, 240),
        'd1': (bt.TimeFrame.Days, 1),
        'M1': (bt.TimeFrame.Months, 1),

    }

    def parse_timeframe(self, timeframe):
        return self.timeframes_mapper[timeframe.value]