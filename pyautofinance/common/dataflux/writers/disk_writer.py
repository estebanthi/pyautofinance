import random
import string
import dill
import datetime as dt

from pyautofinance.common.dataflux.writers.writer import Writer
from pyautofinance.common.config.config import Config


class DiskWriter(Writer):

    def write_ohlcv(self, ohlcv):
        ohlcv_title = str(ohlcv)
        config = Config()
        ohlcv_pathname = config['ohlcv_pathname']
        dataframe = ohlcv.dataframe
        dataframe.to_csv(f"{ohlcv_pathname}/{ohlcv_title}.csv", index=False)

    def write_engine_result(self, engine_result) -> None:
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        config = Config()
        engine_results_pathname = config['engine_results_pathname']
        with open(engine_results_pathname+'/'+filename, 'wb') as file:
            dill.dump(engine_result, file)

    def write_metrics(self, metrics):
        filename = f"{metrics.strategy_name}{dt.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}"
        config = Config()
        live_results_pathname = config['live_results_pathname']
        with open(live_results_pathname + '/' + filename, 'wb') as file:
            dill.dump(metrics, file)
