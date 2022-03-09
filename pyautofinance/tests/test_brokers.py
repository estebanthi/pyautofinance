import unittest
import ccxt

from pyautofinance.common.brokers import BackBroker, CCXTLiveBroker

class TestBrokers(unittest.TestCase):

    def test_backbroker_initialization(self):
        broker = BackBroker(50000, 0.01)
        self.assertEqual(broker._bt_broker.cash, 50000)

    def test_ccxt_live_broker_initialization(self):
        broker = CCXTLiveBroker(ccxt.binance(), 'BTC')
        self.assertTrue(isinstance(broker, CCXTLiveBroker))


if __name__ == '__main__':
    unittest.main()
