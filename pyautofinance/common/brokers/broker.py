import backtrader as bt

from abc import ABC, abstractmethod

from pyautofinance.common.engine.engine_component import EngineComponent


class Broker(EngineComponent):

    @abstractmethod
    def __init__(self):
        # Broker's init parameters may vary
        self._configure()

    @abstractmethod
    def _configure(self) -> None:
        pass

    def attach_to_engine(self, engine):
        engine.cerebro.setbroker(self._bt_broker)


