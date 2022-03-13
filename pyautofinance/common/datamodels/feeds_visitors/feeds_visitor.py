from abc import ABC, abstractmethod

from pyautofinance.common.datamodels.ohlcv import OHLCV


class FeedsVisitor(ABC):

    @abstractmethod
    def check_ohlcv(self, ohlcv: OHLCV) -> bool:
        pass

    @abstractmethod
    def load_ohlcv(self, ohlcv: OHLCV) -> OHLCV:
        pass

    @abstractmethod
    def save_ohlcv(self, ohlcv: OHLCV) -> None:
        pass
