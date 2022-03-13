from abc import abstractmethod

from pyautofinance.common.datamodels.datamodel import Datamodel
from pyautofinance.common.engine.engine_component import EngineComponent


class Dataflux(EngineComponent):
    
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

    def attach_to_engine(self, engine):
        engine.add_dataflux(self)
    