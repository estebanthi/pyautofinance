from abc import ABC, abstractmethod


class DataModelsVisitor(ABC):

    @abstractmethod
    def check_ohlcv(self, ohlcv):
        pass

    @abstractmethod
    def load_ohlcv(self, ohlcv):
        pass

    @abstractmethod
    def save_ohlcv(self, ohlcv):
        pass