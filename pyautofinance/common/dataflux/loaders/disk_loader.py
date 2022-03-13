import pandas as pd

from pyautofinance.common.dataflux.loaders.loader import Loader
from pyautofinance.common.config.config import Config


class DiskLoader(Loader):

    def load_ohlcv(self, ohlcv):
        ohlcv_title = str(ohlcv)
        config = Config()
        ohlcv_pathname = config['ohlcv_pathname']
        ohlcv.dataframe = pd.read_csv(f"{ohlcv_pathname}/{ohlcv_title}.csv")
        return ohlcv
