from enum import Enum
import backtrader as bt


class TimeFrame(Enum):
    s1 = "s1"
    m1 = "m1"
    m5 = "m5"
    m15 = "m15"
    m30 = "m30"
    m45 = "m45"
    h1 = "h1"
    h2 = "h2"
    h4 = "h4"
    d1 = "d1"
    M1 = "M1"

    @classmethod
    def get_bt_timeframe_and_compression_from_timeframe(cls, timeframe):
        timeframes_mapper = {
            cls.s1: (bt.TimeFrame.Seconds, 1),
            cls.m1: (bt.TimeFrame.Minutes, 1),
            cls.m5: (bt.TimeFrame.Minutes, 5),
            cls.m15: (bt.TimeFrame.Minutes, 15),
            cls.m30: (bt.TimeFrame.Minutes, 30),
            cls.m45: (bt.TimeFrame.Minutes, 45),
            cls.h1: (bt.TimeFrame.Minutes, 60),
            cls.h2: (bt.TimeFrame.Minutes, 120),
            cls.h4: (bt.TimeFrame.Minutes, 240),
            cls.d1: (bt.TimeFrame.Days, 1),
            cls.M1: (bt.TimeFrame.Months, 1),
        }
        return timeframes_mapper[timeframe]
