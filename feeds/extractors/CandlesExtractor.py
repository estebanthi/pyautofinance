from abc import ABC, abstractmethod
import pandas as pd
from feeds.options import FeedOptions


class CandlesExtractor(ABC):

    def __init__(self, feed_options: FeedOptions):
        self.feed_options = feed_options

    @abstractmethod
    def extract_candles(self) -> pd.DataFrame:
        """
        Return a DataFrame with prices data in DOHLCV format (Date Open High Low Close Volume)
        """
        pass
