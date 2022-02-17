import pandas as pd
from models.CandlesExtractor.CandlesExtractor import CandlesExtractor
from models.FeedTitle import FeedTitle


class CSVCandlesExtractor(CandlesExtractor):

    def extract_candles(self):
        feed_title = FeedTitle(self.feed_options)
        feed_pathname = feed_title.get_pathname()
        return pd.read_csv(feed_pathname)
