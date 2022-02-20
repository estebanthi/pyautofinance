import pandas as pd
from feeds.extractors.CandlesExtractor import CandlesExtractor
from feeds.FeedTitle import FeedTitle


class CSVCandlesExtractor(CandlesExtractor):

    def _extract_candles(self, feed_options):
        feed_pathname = self._get_feed_pathname(feed_options)
        candles = pd.read_csv(feed_pathname)
        return candles

    @staticmethod
    def _get_feed_pathname(feed_options):
        feed_title = FeedTitle(feed_options)
        feed_pathname = feed_title.get_pathname()
        return feed_pathname
