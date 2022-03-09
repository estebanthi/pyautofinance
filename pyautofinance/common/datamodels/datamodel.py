from abc import ABC, abstractmethod


class DataModel(ABC):

    @abstractmethod
    def accept_visitor_check(self, visitor):
        pass

    @abstractmethod
    def accept_visitor_save(self, visitor):
        pass

    @abstractmethod
    def accept_visitor_load(self, visitor):
        pass
