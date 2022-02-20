from abc import ABC, abstractmethod


class DatafeedGenerator(ABC):

    @abstractmethod
    def generate_datafeed(self):
        pass
