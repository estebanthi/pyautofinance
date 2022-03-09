import backtrader as bt

from abc import abstractmethod

from pyautofinance.common.brokers.broker import Broker


class LiveBroker(Broker):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def _configure(self) -> None:
        pass
