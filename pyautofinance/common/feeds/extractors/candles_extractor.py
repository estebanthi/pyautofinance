from abc import ABC, abstractmethod


class CandlesExtractor(ABC):

    @abstractmethod
    def extract_candles(self, symbol, start_date, end_date, timeframe):
        pass
