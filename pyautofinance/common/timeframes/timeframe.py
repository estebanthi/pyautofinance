from dataclasses import dataclass
from abc import ABC

import backtrader as bt


@dataclass
class TimeFrame(ABC):
    bt_timeframe: bt.TimeFrame
    bt_compression: int
    name: str
    ccxt_name: str = None

    @classmethod
    def total_seconds(cls):
        base_seconds = 0
        if cls.bt_timeframe == bt.TimeFrame.Seconds:
            base_seconds = 1
        if cls.bt_timeframe == bt.TimeFrame.Minutes:
            base_seconds = 60
        if cls.bt_timeframe == bt.TimeFrame.Days:
            base_seconds = 86_400
        if cls.bt_timeframe == bt.TimeFrame.Months:
            base_seconds = 2_678_400
        return base_seconds * cls.bt_compression

