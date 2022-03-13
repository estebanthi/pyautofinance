import pandas as pd

from pyautofinance.common.datamodels.datamodel import DataModel


class OHLCV(DataModel):

    def accept_visitor_check(self, visitor):
        return visitor.check_ohlcv(self)

    def accept_visitor_save(self, visitor):
        visitor.save_ohlcv(self)

    def accept_visitor_load(self, visitor):
        ohlcv = visitor.load_ohlcv(self)
        return ohlcv

    def __init__(self, symbol, start_date, end_date, timeframe, dataframe=pd.DataFrame()):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.timeframe = timeframe
        self.dataframe = dataframe

    def __repr__(self):
        return f"{self.symbol} {self.start_date.strftime('%Y-%m-%d %H-%M-%S')} {self.end_date.strftime('%Y-%m-%d %H-%M-%S')} {self.timeframe.name}"
