from feeds.writers.CSVCandlesWriter import CSVCandlesWriter


class CandlesWriterFactory:

    @staticmethod
    def get_writer(feed, destination):
        if type(destination) is str:
            return CSVCandlesWriter()
