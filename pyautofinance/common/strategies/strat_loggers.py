import backtrader as bt

from abc import ABC, abstractmethod
from termcolor import colored

import time

from pyautofinance.common.options import LoggingOptions


class _StratLogger(ABC):

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

    def log_start(self, logging_data):
        if self.logging_options.start:
            self._log_start(logging_data)

    @abstractmethod
    def _log_start(self, logging_data):
        pass

    def log_stop(self, logging_data):
        if self.logging_options.stop:
            self._log_stop(logging_data)

    @abstractmethod
    def _log_stop(self, logging_data):
        pass


class DefaultStratLogger(_StratLogger):

    def _log(self, txt, logging_data):
        actual_datetime = logging_data.actual_datetime
        print(f"{actual_datetime} : {txt}")

    def _log_every_iter(self, logging_data):
        self.log(f"Close : {logging_data.actual_price}", logging_data)

    def _log_order(self, order, logging_data):
        self.log('Order ref: {} / Type {} / Status {}'.format(
            order.ref,
            self._get_order_type_str_formatted(order),
            self._get_order_status_str_formatted(order)
        ), logging_data)

    @staticmethod
    def _get_order_type_str_formatted(order):
        return colored('Buy', 'green') * order.isbuy() or colored('Sell', 'red')

    @staticmethod
    def _get_order_status_str_formatted(order):
        colors = {bt.Order.Accepted: 'green', bt.Order.Canceled: 'blue', bt.Order.Margin: 'red',
                  bt.Order.Submitted: 'blue', bt.Order.Rejected: 'red', bt.Order.Completed: 'yellow'}
        if order.status in colors:
            return colored(order.getstatusname(), colors[order.status])
        return colored(order.getstatusname(), 'white')

    def _log_trade(self, trade, logging_data):
        color = self._get_trade_display_color(trade)
        self.log(colored('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                         (trade.pnl, trade.pnlcomm), color), logging_data)

    @staticmethod
    def _get_trade_display_color(trade):
        return "green" if trade.pnlcomm > 0 else "red"

    def _log_total_profit(self, total_profit, logging_data):
        color = self._get_total_profit_display_color(total_profit)
        self.log(colored("TOTAL PROFIT : %.2f" % total_profit, color), logging_data)

    @staticmethod
    def _get_total_profit_display_color(total_profit):
        return 'green' if total_profit > 0 else 'red'

    def _log_long(self, logging_data):
        actual_price = logging_data.actual_price
        stop_price = logging_data.long_stop_price
        take_profit_price = logging_data.long_take_profit_price

        long_str = "LONG CREATED : "
        common_str = self._get_long_or_short_string_to_log(actual_price, stop_price, take_profit_price)

        self.log(long_str + common_str, logging_data)

    def _log_short(self, logging_data):
        actual_price = logging_data.actual_price
        stop_price = logging_data.short_stop_price
        take_profit_price = logging_data.short_take_profit_price

        short_str = "SHORT CREATED : "
        common_str = self._get_long_or_short_string_to_log(actual_price, stop_price, take_profit_price)

        self.log(short_str + common_str, logging_data)

    def _get_long_or_short_string_to_log(self, actual_price, stop_price, take_profit_price):
        main_str = self._get_main_str(actual_price)
        stop_str = self._get_stop_str(stop_price)
        take_profit_str = self._get_take_profit_str(take_profit_price)

        return main_str + stop_str + take_profit_str

    @staticmethod
    def _get_main_str(actual_price):
        return f"\nMain : {actual_price}"

    @staticmethod
    def _get_stop_str(stop_price):
        if stop_price:
            return f"\nStop : {stop_price}"
        return ''

    @staticmethod
    def _get_take_profit_str(take_profit_price):
        if take_profit_price:
            return f"\nTake Profit : {take_profit_price}"
        return ''

    def _log_start(self, logging_data):
        self.log(f"---STARTING---\nInitial cash : {logging_data.cash}", logging_data)

    def _log_stop(self, logging_data):
        self.log(f"---ENDING---\nFinal cash : {logging_data.cash}\n"
                 f"Total profit : {logging_data.cash - logging_data.initial_cash}",
                 logging_data)


class TelegramLogger(_StratLogger):

    def __init__(self, telegram_bot, logging_options=LoggingOptions()):
        super().__init__(logging_options)
        self._telegram_bot = telegram_bot

    def _log(self, txt, logging_data):
        actual_datetime = logging_data.actual_datetime
        self._telegram_bot.send_message(f"{actual_datetime} : {txt}")
        time.sleep(0.1)

    def _log_every_iter(self, logging_data):
        self.log(f"Close : {logging_data.actual_price}", logging_data)

    def _log_order(self, order, logging_data):
        self.log('Order ref: {} / Type {} / Status {}'.format(
            order.ref,
            self._get_order_type_str_formatted(order),
            self._get_order_status_str_formatted(order)
        ), logging_data)

    @staticmethod
    def _get_order_type_str_formatted(order):
        return 'Buy' * order.isbuy() or 'Sell'

    @staticmethod
    def _get_order_status_str_formatted(order):
        return order.getstatusname()

    def _log_trade(self, trade, logging_data):
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm), logging_data)

    def _log_total_profit(self, total_profit, logging_data):
        self.log("TOTAL PROFIT : %.2f" % total_profit, logging_data)

    def _log_long(self, logging_data):
        actual_price = logging_data.actual_price
        stop_price = logging_data.long_stop_price
        take_profit_price = logging_data.long_take_profit_price

        long_str = "LONG CREATED : "
        common_str = self._get_long_or_short_string_to_log(actual_price, stop_price, take_profit_price)

        self.log(long_str + common_str, logging_data)

    def _log_short(self, logging_data):
        actual_price = logging_data.actual_price
        stop_price = logging_data.short_stop_price
        take_profit_price = logging_data.short_take_profit_price

        short_str = "SHORT CREATED : "
        common_str = self._get_long_or_short_string_to_log(actual_price, stop_price, take_profit_price)

        self.log(short_str + common_str, logging_data)

    def _get_long_or_short_string_to_log(self, actual_price, stop_price, take_profit_price):
        main_str = self._get_main_str(actual_price)
        stop_str = self._get_stop_str(stop_price)
        take_profit_str = self._get_take_profit_str(take_profit_price)

        return main_str + stop_str + take_profit_str

    @staticmethod
    def _get_main_str(actual_price):
        return f"\nMain : {actual_price}"

    @staticmethod
    def _get_stop_str(stop_price):
        if stop_price:
            return f"\nStop : {stop_price}"
        return ''

    @staticmethod
    def _get_take_profit_str(take_profit_price):
        if take_profit_price:
            return f"\nTake Profit : {take_profit_price}"
        return ''

    def _log_start(self, logging_data):
        self.log(f"---STARTING---\nInitial cash : {logging_data.cash}", logging_data)

    def _log_stop(self, logging_data):
        self.log(f"---ENDING---\nFinal cash : {logging_data.cash}\nTotal profit : {logging_data.total_profit}",
                 logging_data)
