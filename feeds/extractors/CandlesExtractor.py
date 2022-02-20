from abc import ABC, abstractmethod
import pandas as pd
from feeds.options import FeedOptions
from feeds.formatters.SimpleCandlesFormatter import SimpleCandlesFormatter
from feeds.filterers.SimpleCandlesFilterer import SimpleCandlesFilterer


class CandlesExtractor(ABC):

    def get_formatted_and_filtered_candles(self,
                                           feed_options,
                                           formatter=SimpleCandlesFormatter(),
                                           filterer=SimpleCandlesFilterer()
                                           ):
        extracted_candles = self._extract_candles(feed_options)

        formatted_candles = formatter.format_candles(extracted_candles, feed_options)
        filtered_and_formatted_candles = filterer.filter_candles(formatted_candles, feed_options)

        return filtered_and_formatted_candles

    @abstractmethod
    def _extract_candles(self, feed_options: FeedOptions) -> pd.DataFrame:
        """
        Return a DataFrame with prices data in DOHLCV format (Date Open High Low Close Volume)
        """
        pass
