from feeds.writers.CandlesWriter import CandlesWriter


class CSVCandlesWriter(CandlesWriter):

    def write(self, feed, destination):
        feed.to_csv(destination)