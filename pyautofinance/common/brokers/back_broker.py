import backtrader as bt

from pyautofinance.common.brokers.broker import Broker


class BackBroker(Broker):

    def __init__(self, cash, commission):
        self._cash = cash
        self._commission = commission
        self._bt_broker = bt.BackBroker()
        super().__init__()

    def _configure(self):
        self._bt_broker.set_cash(self._cash)
        self._bt_broker.setcommission(self._commission)
