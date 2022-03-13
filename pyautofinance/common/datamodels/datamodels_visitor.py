from abc import ABC, abstractmethod

from pyautofinance.common.datamodels.datamodel import DataModel


class DataModelsVisitor(ABC):

    @abstractmethod
    def check(self, datamodel: DataModel) -> bool:
        pass

    @abstractmethod
    def load(self, datamodel: DataModel) -> DataModel:
        pass

    @abstractmethod
    def save(self, datamodel: DataModel) -> None:
        pass
