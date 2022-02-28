from abc import ABC, abstractmethod


class Tester(ABC):

    @abstractmethod
    def test(self, engine_options):
        pass

    @abstractmethod
    def multitest(self, engine_options, symbols):
        pass
