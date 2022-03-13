import pandas as pd

from pyautofinance.common.datamodels.datamodel import Datamodel


class OHLCV(Datamodel):

    def __init__(self, symbol, start_date, end_date, timeframe, dataframe=pd.DataFrame()):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.timeframe = timeframe
        self.dataframe = dataframe

    def __repr__(self):
        return f"{self.symbol} {self.start_date.strftime('%Y-%m-%d %H-%M-%S')} {self.end_date.strftime('%Y-%m-%d %H-%M-%S')} {self.timeframe.name}"
