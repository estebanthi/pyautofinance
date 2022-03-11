from abc import ABC, abstractmethod

from pyautofinance.common.options import LoggingOptions


class StratLogger(ABC):

    def __init__(self, logging_options=LoggingOptions()):
        self.logging = True
        self.logging_options = logging_options

    def disable(self):
        self.logging = False

    def log(self, txt, logging_data):
        if self.logging:
            self._log(txt, logging_data)

    @abstractmethod
    def _log(self, txt, logging_data):
        pass

    def log_every_iter(self, logging_data):
        if self.logging_options.every_iter:
            self._log_every_iter(logging_data)

    @abstractmethod
    def _log_every_iter(self, logging_data):
        pass

    def log_order(self, order, logging_data):
        if self.logging_options.orders:
            self._log_order(order, logging_data)

    @abstractmethod
    def _log_order(self, order, logging_data):
        pass

    def log_trade(self, trade, logging_data):
        if self.logging_options.trades:
            self._log_trade(trade, logging_data)

    @abstractmethod
    def _log_trade(self, trade, logging_data):
        pass

    def log_total_profit(self, total_profit, logging_data):
        if self.logging_options.total_profit:
            self._log_total_profit(total_profit, logging_data)

    @abstractmethod
    def _log_total_profit(self, total_profit, logging_data):
        pass

    def log_long(self, logging_data):
        if self.logging_options.orders:
            self._log_long(logging_data)

    @abstractmethod
    def _log_long(self, logging_data):
        pass

    def log_short(self, logging_data):
        if self.logging_options.orders:
            self._log_short(logging_data)

    @abstractmethod
    def _log_long(self, logging_data):
        pass

    def log_start(self):
        if self.logging_options.start:
            self._log_start()

    @abstractmethod
    def _log_start(self):
        pass

    def log_stop(self, logging_data):
        if self.logging_options.stop:
            self._log_stop(logging_data)

    @abstractmethod
    def _log_stop(self, logging_data):
        pass