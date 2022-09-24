from pyautofinance.common.feeds.datafeed import Datafeed


class MultiDatafeed(Datafeed):

        def __init__(self, symbol, start_date, timeframe, *datafeeds):
            super().__init__(symbol, start_date, timeframe)
            self.datafeeds = datafeeds

        def attach_to_engine(self, engine):
            for datafeed in self.datafeeds:
                datafeed.attach_to_engine(engine)
