from dataclasses import dataclass
from abc import ABC

import backtrader as bt


@dataclass
class TimeFrame(ABC):
    bt_timeframe: bt.TimeFrame
    bt_compression: int
    name: str
    ccxt_name: str = None

    def __post_init__(self):
        self.total_seconds = self._get_total_seconds()

    def _get_total_seconds(self):
        base_seconds = 0
        if self.bt_timeframe == bt.TimeFrame.Seconds:
            base_seconds = 1
        if self.bt_timeframe == bt.TimeFrame.Minutes:
            base_seconds = 60
        if self.bt_timeframe == bt.TimeFrame.Days:
            base_seconds = 86_400
        if self.bt_timeframe == bt.TimeFrame.Months:
            base_seconds = 2_678_400
        return base_seconds*self.bt_compression
