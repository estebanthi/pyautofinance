import datetime as dt
import unittest
import backtrader as bt
import ccxt

from pyautofinance.common.timeframes import h4
from pyautofinance.common.feeds import CCXTDatafeed


class TestCCXTDatafeed(unittest.TestCase):

    symbol = 'BTC-EUR'
    start_date = dt.datetime(2020, 1, 1)
    timeframe = h4

    def test_initialization(self):
        datafeed = CCXTDatafeed(self.symbol, self.start_date, self.timeframe, ccxt.binance(), 'BTC')
        bt_datafeed = datafeed._bt_datafeed
        self.assertIsInstance(bt_datafeed, bt.feeds.DataBase)


if __name__ == '__main__':
    unittest.main()
