import backtrader as bt
import datetime as dt

from abc import abstractmethod
from dataclasses import dataclass

from pyautofinance.common.strategies.strat_loggers import DefaultStratLogger


class Strategy(bt.Strategy):
    params = (
        ('logging', False),
        ('longs_enabled', True),
        ('shorts_enabled', True),
        ('stop_loss', 0),
        ('risk_reward', 0),
        ('logger', DefaultStratLogger)
    )

    def __init__(self):
        self.orders_ref = list()
        self.total_profit = 0
        self.logger = self.p.logger(self.p.logging)

    # Strategy constructor, use it instead of __init__
    def _init_strat(self) -> None:
        pass

    def _get_logging_data(self):
        @dataclass
        class LoggingData:
            actual_datetime: dt.datetime = self.datas[0].datetime.datetime(0)
            actual_price: float = self.datas[0].close[0]

            long_stop_price: float = self._get_long_stop_loss_price()
            short_stop_price: float = self._get_short_stop_loss_price()
            long_take_profit_price: float = self._get_long_take_profit_price()
            short_take_profit_price: float = self._get_short_take_profit_price()

        return LoggingData()

    @abstractmethod
    def _open_short_condition(self) -> bool:
        pass

    @abstractmethod
    def _open_long_condition(self) -> bool:
        pass

    @abstractmethod
    def _close_short_condition(self) -> bool:
        pass

    @abstractmethod
    def _close_long_condition(self) -> bool:
        pass

    @abstractmethod
    def _get_long_stop_loss_price(self) -> float:
        return 0

    @abstractmethod
    def _get_long_take_profit_price(self) -> float:
        return 0

    @abstractmethod
    def _get_short_stop_loss_price(self) -> float:
        return 0

    @abstractmethod
    def _get_short_take_profit_price(self) -> float:
        return 0

    def notify_data(self, data, status, *args, **kwargs):
        status = data._getstatusname(status)
        if status == data.LIVE:
            self.logger.log_data_live(self._get_logging_data())
        else:
            self.logger.log_data_not_live(status, self._get_logging_data())

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.logger.log_trade(trade, self._get_logging_data())

        self.total_profit += trade.pnlcomm
        self.logger.log_total_profit(self.total_profit, self._get_logging_data())

    def notify_order(self, order):
        self.logger.log_order(order, self._get_logging_data())
        self._del_order_if_not_alive(order)

    def _del_order_if_not_alive(self, order):
        if not order.alive() and order.ref in self.orders_ref:
            self.orders_ref.remove(order.ref)

    def next(self):
        self.logger.log(f"Close : {self.datas[0].close[0]}", self._get_logging_data())

        if self.orders_ref:
            return

        if not self.position:
            self._not_yet_in_market()
        else:
            self._in_market()

    def _not_yet_in_market(self):
        if self._long_condition():
            stop_price = self._get_long_stop_loss_price()
            take_profit_price = self._get_long_take_profit_price()

            self._go_long(stop_price, take_profit_price)
            self.logger.log_long(self._get_logging_data())

        if self._short_condition():
            stop_price = self._get_short_stop_loss_price()
            take_profit_price = self._get_short_take_profit_price()

            self._go_short(stop_price, take_profit_price)
            self.logger.log_short(self._get_logging_data())

    def _long_condition(self):
        return self._open_long_condition() and self.params.longs_enabled

    def _short_condition(self):
        return self._open_short_condition() and self.params.shorts_enabled

    def _go_long(self, stop_price, take_profit_price):
        orders = self._get_long_orders_from_stop_and_take_profit(stop_price, take_profit_price)
        self.orders_ref = [order.ref for order in orders]

    def _get_long_orders_from_stop_and_take_profit(self, stop_price, take_profit_price):
        orders = []
        ACTUAL_PRICE = self.datas[0].close[0]
        if stop_price != ACTUAL_PRICE and take_profit_price != ACTUAL_PRICE:
            orders = self.buy_bracket(price=ACTUAL_PRICE, stopprice=stop_price, limitprice=take_profit_price)
        elif stop_price != ACTUAL_PRICE and take_profit_price == ACTUAL_PRICE:
            orders = [self.buy(), self.sell(exectype=bt.Order.Stop, price=stop_price)]
        elif stop_price == ACTUAL_PRICE and take_profit_price != ACTUAL_PRICE:
            orders = [self.buy(), self.sell(exectype=bt.Order.Limit, price=take_profit_price)]
        else:
            orders = [self.buy()]
        return orders

    def _go_short(self, stop_price, take_profit_price):
        orders = self._get_short_orders_from_stop_and_take_profit(stop_price, take_profit_price)
        self.orders_ref = [order.ref for order in orders]

    def _get_short_orders_from_stop_and_take_profit(self, stop_price, take_profit_price):
        orders = []
        ACTUAL_PRICE = self.datas[0].close[0]
        if stop_price != ACTUAL_PRICE and take_profit_price != ACTUAL_PRICE:
            orders = self.sell_bracket(price=ACTUAL_PRICE, stopprice=stop_price, limitprice=take_profit_price)
        elif stop_price != ACTUAL_PRICE and take_profit_price == ACTUAL_PRICE:
            orders = [self.sell(), self.buy(exectype=bt.Order.Stop, price=stop_price)]
        elif stop_price == ACTUAL_PRICE and take_profit_price != ACTUAL_PRICE:
            orders = [self.sell(), self.buy(exectype=bt.Order.Limit, price=take_profit_price)]
        else:
            orders = [self.sell()]
        return orders