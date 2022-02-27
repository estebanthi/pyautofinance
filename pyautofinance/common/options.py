import backtrader as bt
import datetime as dt
import ccxt

from dataclasses import dataclass
from enum import Enum

from pyautofinance.common.exceptions.feeds import EndDateBeforeStartDate
from pyautofinance.common.feeds.formatters import CandlesFormatter
from pyautofinance.common.feeds.filterers import CandlesFilterer
from pyautofinance.common.timeframes import TimeFrame


class DateFormat(Enum):
    FEED_FILENAME = "%Y-%m-%d_%H-%M-%S"


class Market(Enum):
    STOCKS = "STOCKS"
    FOREX = "FOREX"
    CRYPTO = "CRYPTO"


@dataclass
class MarketOptions:
    market: Market
    symbol: str


@dataclass
class TimeOptions:
    start_date: dt.datetime
    timeframe: TimeFrame
    end_date: dt.datetime = None  # Not useful for live datafeed

    def __post_init__(self):
        if self.end_date:
            if self.end_date < self.start_date:
                raise EndDateBeforeStartDate


@dataclass
class FeedOptions:
    market_options: MarketOptions
    time_options: TimeOptions


@dataclass
class BrokerOptions:
    cash: int = None  # Parameters may vary for live or backtesting config
    commission: float = None
    currency: str = None
    exchange: ccxt.Exchange = None


@dataclass
class WritingOptions:
    candles_destination: any = None
    results_destination: any = None


@dataclass
class FormattingOptions:
    formatter: CandlesFormatter


@dataclass
class FilteringOptions:
    filterer: CandlesFilterer


@dataclass
class EngineOptions:
    broker_options: BrokerOptions
    feed_options: FeedOptions
    strategies: list
    sizer: bt.Sizer
    analyzers: list = None
    observers: list = None
    timers: list = None
    writing_options: WritingOptions = None
    formatting_options: FormattingOptions = None
    filtering_options: FilteringOptions = None


@dataclass
class LoggingOptions:
    every_iter: bool = True
    trades: bool = True
    orders: bool = True
    total_profit: bool = True
    start: bool = True
    stop: bool = True
