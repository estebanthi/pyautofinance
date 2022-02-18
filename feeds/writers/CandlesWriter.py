from abc import ABC, abstractmethod
from feeds.writers.CandlesWriterFactory import CandlesWriterFactory


class CandlesWriter(ABC):
    factory = CandlesWriterFactory()

    def write(self, feed, destination):
        writer = self.factory.get_writer(feed, destination)
        writer.write(feed, destination)
