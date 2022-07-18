import os

from pyautofinance.common.strategies.strat_loggers.default_logger import DefaultStratLogger
from pyautofinance.common.config.config import Config
from pyautofinance.common.options.logging_options import LoggingOptions


class FileLogger(DefaultStratLogger):

    def __init__(self, logging_options=LoggingOptions(), file_path=f'{Config()["logs_pathname"]}/log.txt'):
        super().__init__(logging_options)
        self._file_path = file_path

    def _log(self, txt, logging_data):
        if logging_data:
            actual_datetime = logging_data.actual_datetime
            text = f"{actual_datetime} : {txt}"
        else:
            text = txt
        print(text)
        self._write_to_file(text)

    def _write_to_file(self, text):
        if not os.path.isfile(self._file_path):
            with open(self._file_path, 'w') as file:
                pass
        with open(self._file_path, 'a') as f:
            f.write(f"{text}\n")
