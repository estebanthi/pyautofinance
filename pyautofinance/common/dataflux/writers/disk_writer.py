from pyautofinance.common.dataflux.writers.writer import Writer
from pyautofinance.common.config.config import Config


class DiskWriter(Writer):

    def write_ohlcv(self, ohlcv):
        ohlcv_title = str(ohlcv)
        config = Config()
        ohlcv_pathname = config['ohlcv_pathname']
        dataframe = ohlcv.dataframe
        dataframe.to_csv(f"{ohlcv_pathname}/{ohlcv_title}.csv", index=False)
