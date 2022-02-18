class CSVCandlesWriter:
    def write(self, feed, destination):
        feed.to_csv(destination)