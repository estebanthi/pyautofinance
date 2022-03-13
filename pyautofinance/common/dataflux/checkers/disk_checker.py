import os

from pyautofinance.common.dataflux.checkers.checker import Checker
from pyautofinance.common.config.config import Config


class DiskChecker(Checker):

    def check_ohlcv(self, ohlcv):
        ohlcv_title = str(ohlcv)
        config = Config()
        ohlcv_pathname = config['ohlcv_pathname']

        if os.path.exists(f"{ohlcv_pathname}/{ohlcv_title}.csv"):
            return True
        return False
