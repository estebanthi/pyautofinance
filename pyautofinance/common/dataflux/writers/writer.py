from abc import ABC, abstractmethod

from pyautofinance.common.datamodels.datamodel import Datamodel
from pyautofinance.common.datamodels.ohlcv import OHLCV


class Writer(ABC):

    def write(self, datamodel: Datamodel):
        if isinstance(datamodel, OHLCV):
            self.write_ohlcv(datamodel)

    @abstractmethod
    def write_ohlcv(self, ohlcv: OHLCV) -> None:
        pass
