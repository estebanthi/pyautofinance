import backtrader as bt

from pyautofinance.common.timeframes.timeframe import TimeFrame


class s1(TimeFrame):
    name = '1s'
    ccxt_name = '1s'
    bt_timeframe = bt.TimeFrame.Seconds
    bt_compression = 1


class m1(TimeFrame):
    name = '1m'
    ccxt_name = '1m'
    bt_timeframe = bt.TimeFrame.Minutes
    bt_compression = 1


class m5(TimeFrame):
    name = '5m'
    ccxt_name = '5m'
    bt_timeframe = bt.TimeFrame.Minutes
    bt_compression = 5


class m15(TimeFrame):
    name = '15m'
    ccxt_name = '15m'
    bt_timeframe = bt.TimeFrame.Minutes
    bt_compression = 15


class m30(TimeFrame):
    name = '30m'
    ccxt_name = '30m'
    bt_timeframe = bt.TimeFrame.Minutes
    bt_compression = 30


class m45(TimeFrame):
    name = '45m'
    ccxt_name = '45m'
    bt_timeframe = bt.TimeFrame.Minutes
    bt_compression = 45


class h1(TimeFrame):
    name = '1h'
    ccxt_name = '1h'
    bt_timeframe = bt.TimeFrame.Minutes
    bt_compression = 60


class h2(TimeFrame):
    name = '2h'
    ccxt_name = '2h'
    bt_timeframe = bt.TimeFrame.Minutes
    bt_compression = 120


class h4(TimeFrame):
    name = '4h'
    ccxt_name = '4h'
    bt_timeframe = bt.TimeFrame.Minutes
    bt_compression = 240


class d1(TimeFrame):
    name = '1d'
    ccxt_name = '1d'
    bt_timeframe = bt.TimeFrame.Days
    bt_compression = 1


class M1(TimeFrame):
    name = '1M'
    ccxt_name = '1M'
    bt_timeframe = bt.TimeFrame.Months
    bt_compression = 1
