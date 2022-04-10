from abc import ABC, abstractmethod

from pyautofinance.common.datamodels.datamodel import Datamodel
from pyautofinance.common.datamodels.ohlcv import OHLCV
from pyautofinance.common.results.engine_result import EngineResult
from pyautofinance.common.metrics.live_metrics import LiveMetricsCollection


class Writer(ABC):

    def write(self, datamodel: Datamodel):
        if isinstance(datamodel, OHLCV):
            self.write_ohlcv(datamodel)
        if isinstance(datamodel, EngineResult):
            self.write_engine_result(datamodel)
        if isinstance(datamodel, LiveMetricsCollection):
            self.write_live_metrics_collection(datamodel)

    @abstractmethod
    def write_ohlcv(self, ohlcv: OHLCV) -> None:
        pass

    @abstractmethod
    def write_engine_result(self, engine_result: EngineResult) -> None:
        pass

    @abstractmethod
    def write_live_metrics_collection(self, live_metrics_collection: LiveMetricsCollection) -> None:
        pass
