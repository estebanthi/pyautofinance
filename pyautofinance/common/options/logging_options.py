from dataclasses import dataclass


@dataclass
class LoggingOptions:
    every_iter: bool = True
    trades: bool = True
    orders: bool = True
    total_profit: bool = True
    start: bool = True
    stop: bool = True
