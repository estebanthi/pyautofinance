import os
import pandas as pd

from pyautofinance.common.datamodels.datamodels_visitor import DataModelsVisitor
from pyautofinance.common.config.config import Config


class CSVDataModelsVisitor(DataModelsVisitor):

    def check_ohlcv(self, ohlcv):
        ohlcv_title = str(ohlcv)
        config = Config()
        ohlcv_pathname = config['ohlcv_pathname']

        if os.path.exists(f"{ohlcv_pathname}/{ohlcv_title}.csv"):
            return True
        return False

    def load_ohlcv(self, ohlcv):
        ohlcv_title = str(ohlcv)
        config = Config()
        ohlcv_pathname = config['ohlcv_pathname']
        ohlcv.dataframe = pd.read_csv(f"{ohlcv_pathname}/{ohlcv_title}.csv")
        return ohlcv.dataframe

    def save_ohlcv(self, ohlcv):
        ohlcv_title = str(ohlcv)
        config = Config()
        ohlcv_pathname = config['ohlcv_pathname']

        dataframe = ohlcv.dataframe
        dataframe.to_csv(f"{ohlcv_pathname}/{ohlcv_title}.csv", index=False)
