from dataclasses import dataclass
from enum import Enum
import datetime as dt


class TradeSide(Enum):
    LONG = 'LONG'
    SHORT = 'SHORT'


@dataclass
class Trade:
    ref: int
    symbol: str
    side: TradeSide
    datein: dt.datetime
    pricein: float
    dateout: dt.datetime
    priceout: float
    change_percent: float
    pnl: float
    pnl_percent: float
    size: float
    value: float
    nbars: int
    pnl_per_bar: float
    mfe_percent: float
    mae_percent: float
