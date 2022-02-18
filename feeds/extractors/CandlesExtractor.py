from abc import ABC, abstractmethod
import pandas as pd
from feeds.options import FeedOptions


class CandlesExtractor(ABC):

    @abstractmethod
    def extract_candles(self, feed_options: FeedOptions) -> pd.DataFrame:
        """
        Return a DataFrame with prices data in DOHLCV format (Date Open High Low Close Volume)
        """
        pass
