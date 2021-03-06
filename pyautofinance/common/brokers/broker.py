from abc import abstractmethod

from pyautofinance.common.engine.engine_component import EngineComponent


class Broker(EngineComponent):

    @abstractmethod
    def __init__(self):
        self._configure()

    @abstractmethod
    def _configure(self) -> None:
        pass

    def attach_to_engine(self, engine):
        engine.cerebro.setbroker(self._bt_broker)


