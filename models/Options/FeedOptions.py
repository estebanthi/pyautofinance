from dataclasses import dataclass
from models.Options.MarketOptions import MarketOptions
from models.Options.TimeOptions import TimeOptions


@dataclass
class FeedOptions:
    market_options: MarketOptions
    time_options: TimeOptions

