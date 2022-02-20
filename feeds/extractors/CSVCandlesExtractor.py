import pandas as pd
from feeds.extractors.CandlesExtractor import CandlesExtractor
from feeds.FeedTitle import FeedTitle


class CSVCandlesExtractor(CandlesExtractor):

    def _extract_candles(self, feed_options):
        feed_title = FeedTitle(feed_options)
        feed_pathname = feed_title.get_pathname()
        candles = pd.read_csv(feed_pathname)
        return candles
