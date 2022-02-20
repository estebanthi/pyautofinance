class CSVCandlesWriter:

    @staticmethod
    def _write(feed, destination):
        feed.to_csv(destination)