from abc import ABC, abstractmethod


class CandlesWriter(ABC):

    @abstractmethod
    def write(self, feed, destination):
        """
        Write a feed to a destination
        """
        pass
