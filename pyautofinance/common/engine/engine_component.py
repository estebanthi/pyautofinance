from abc import ABC, abstractmethod


class EngineComponent(ABC):

    @abstractmethod
    def attach_to_engine(self, engine):
        """ Operates some operations on the engine """
        pass
