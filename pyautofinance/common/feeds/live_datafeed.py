from pyautofinance.common.feeds.datafeed import Datafeed
from abc import ABC, abstractmethod


class LiveDatafeed(Datafeed):

    def __init__(self, symbol, start_date, timeframe):
        super().__init__(symbol, start_date, timeframe)

    @abstractmethod
    def _get(self):
        pass
