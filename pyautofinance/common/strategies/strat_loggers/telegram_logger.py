import time

from pyautofinance.common.strategies.strat_loggers.strat_logger import StratLogger
from pyautofinance.common.strategies.strat_loggers import LoggingOptions


class TelegramLogger(StratLogger):

    def __init__(self, telegram_bot, logging_options=LoggingOptions()):
        super().__init__(logging_options)
        self._telegram_bot = telegram_bot

    def _log(self, txt, logging_data):
        if logging_data:
            actual_datetime = logging_data.actual_datetime
            self._telegram_bot.send_message(f"{actual_datetime} : {txt}")
            time.sleep(0.1)
        else:
            self._telegram_bot.send_message(txt)

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

    def _log_start(self):
        self.log(f"---STARTING---", None)

    def _log_stop(self, logging_data):
        self.log(f"---ENDING---\nFinal cash : {logging_data.cash}\nTotal profit : {logging_data.total_profit}",
                 logging_data)
