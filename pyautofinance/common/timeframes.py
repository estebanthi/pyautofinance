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


class s1(TimeFrame):
    def __init__(self):
        super().__init__(bt.TimeFrame.Seconds, 1, 's1', '1s')


class m1(TimeFrame):
    def __init__(self):
        super().__init__(bt.TimeFrame.Minutes, 1, 'm1', '1m')


class m5(TimeFrame):
    def __init__(self):
        super().__init__(bt.TimeFrame.Minutes, 5, 'm5' '5m')


class m15(TimeFrame):
    def __init__(self):
        super().__init__(bt.TimeFrame.Minutes, 15, 'm15', '15m')


class m30(TimeFrame):
    def __init__(self):
        super().__init__(bt.TimeFrame.Minutes, 30, 'm30', '30m')


class m45(TimeFrame):
    def __init__(self):
        super().__init__(bt.TimeFrame.Minutes, 45, 'm45', '45m')


class h1(TimeFrame):
    def __init__(self):
        super().__init__(bt.TimeFrame.Minutes, 60, 'h1', '1h')


class h2(TimeFrame):
    def __init__(self):
        super().__init__(bt.TimeFrame.Minutes, 120, 'h2', '2h')


class h4(TimeFrame):
    def __init__(self):
        super().__init__(bt.TimeFrame.Minutes, 240, 'h4', '4h')


class d1(TimeFrame):
    def __init__(self):
        super().__init__(bt.TimeFrame.Days, 5, 'd1', '1d')


class M1(TimeFrame):
    def __init__(self):
        super().__init__(bt.TimeFrame.Minutes, 5, 'M1', '1M')
