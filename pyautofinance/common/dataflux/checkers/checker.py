from abc import ABC, abstractmethod

from pyautofinance.common.datamodels.datamodel import Datamodel
from pyautofinance.common.datamodels.ohlcv import OHLCV


class Checker(ABC):

    def check(self, datamodel: Datamodel):
        result = False

        if isinstance(datamodel, OHLCV):
            result = self.check_ohlcv(datamodel)

        return result

    @abstractmethod
    def check_ohlcv(self, ohlcv: OHLCV) -> bool:
        pass
