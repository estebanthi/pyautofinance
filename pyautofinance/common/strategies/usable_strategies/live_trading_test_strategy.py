from pyautofinance.common.strategies.bracket_strategy import BracketStrategy


class LiveTradingTestStrategy(BracketStrategy):

    def _open_long_condition(self) -> bool:
        return True

    def _open_short_condition(self) -> bool:
        return False
