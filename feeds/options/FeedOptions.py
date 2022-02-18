from dataclasses import dataclass
from feeds.options.MarketOptions import MarketOptions
from feeds.options.TimeOptions import TimeOptions


@dataclass
class FeedOptions:
    market_options: MarketOptions
    time_options: TimeOptions

