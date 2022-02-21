from abc import ABC


class CSVCandlesWriter:

    @staticmethod
    def write(feed, destination):
        feed.to_csv(destination)


class _CandlesWriterFactory:

    @staticmethod
    def get_writer(feed, destination):
        if type(destination) is str:
            return CSVCandlesWriter()


class CandlesWriter(ABC):
    factory = _CandlesWriterFactory()

    def write(self, feed, destination):
        writer = self.factory.get_writer(feed, destination)
        writer.write(feed, destination)
