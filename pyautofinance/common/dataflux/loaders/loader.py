from abc import ABC, abstractmethod

from pyautofinance.common.datamodels.datamodel import Datamodel
from pyautofinance.common.datamodels.ohlcv import OHLCV


class Loader(ABC):

    def load(self, datamodel: Datamodel):
        result = None

        if isinstance(datamodel, OHLCV):
            result = self.load_ohlcv(datamodel)

        return result

    @abstractmethod
    def load_ohlcv(self, ohlcv: OHLCV) -> OHLCV:
        pass
