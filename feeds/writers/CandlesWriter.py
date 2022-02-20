from abc import ABC, abstractmethod
from feeds.writers.CandlesWriterFactory import CandlesWriterFactory


class CandlesWriter(ABC):
    factory = CandlesWriterFactory()

    def write(self, feed, destination):
        writer = self.factory._get_writer(feed, destination)
        writer._write(feed, destination)
