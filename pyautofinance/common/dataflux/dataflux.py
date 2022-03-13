from abc import ABC, abstractmethod

from pyautofinance.common.datamodels.datamodel import Datamodel


class Dataflux(ABC):
    
    @abstractmethod
    def __init__(self, writer, loader, checker):
        self._writer = writer
        self._loader = loader
        self._checker = checker
        
    def load(self, datamodel: Datamodel):
        return self._loader.load(datamodel)
    
    def write(self, datamodel: Datamodel):
        self._writer.write(datamodel)
        
    def check(self, datamodel: Datamodel):
        return self._checker.check(datamodel)
    