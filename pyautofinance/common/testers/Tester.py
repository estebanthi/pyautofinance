from abc import ABC, abstractmethod


class Tester(ABC):

    @abstractmethod
    def test(self, testing_options):
        pass
