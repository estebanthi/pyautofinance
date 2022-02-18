from dataclasses import dataclass
from enums import Market


@dataclass
class MarketOptions:
    market: Market
    symbol: str
