import unittest
import ccxt
import backtrader as bt
from ccxtbt import CCXTBroker

from pyautofinance.common.broker.BrokersFactory import BrokersFactory
from pyautofinance.common.options import BrokerOptions

class TestBroker(unittest.TestCase):

    bt_broker_options = BrokerOptions(cash=100000, commission=2)
    ccxt_broker_options = BrokerOptions(exchange=ccxt.binance(), currency='EUR')
    factory = BrokersFactory()

    def test_broker_factory_for_bt(self):
        broker = self.factory.get_broker(self.bt_broker_options)

        self.assertEqual(type(broker), bt.brokers.BackBroker)

    def test_broker_factory_for_ccxt(self):
        broker = self.factory.get_broker(self.ccxt_broker_options)

        self.assertEqual(type(broker), CCXTBroker)

if __name__ == '__main__':
    unittest.main()
