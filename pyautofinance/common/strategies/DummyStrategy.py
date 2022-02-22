from pyautofinance.common.strategies.Strategy import Strategy


class DummyStrategy(Strategy):

    def open_short_condition(self) -> bool:
        pass

    def open_long_condition(self) -> bool:
        pass

    def close_short_condition(self) -> bool:
        pass

    def close_long_condition(self) -> bool:
        pass

    def get_long_stop_loss_price(self):
        pass

    def get_long_take_profit_price(self):
        pass

    def get_short_stop_loss_price(self):
        pass

    def get_short_take_profit_price(self):
        pass