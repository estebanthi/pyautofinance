from feeds.writers.CSVCandlesWriter import CSVCandlesWriter


class CandlesWriterFactory:
    def get_writer(self, feed, destination):
        if type(destination) is str:
            return CSVCandlesWriter()
