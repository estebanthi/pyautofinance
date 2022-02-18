from dataclasses import dataclass
import datetime as dt
from enums import TimeFrame


@dataclass
class TimeOptions:
    start_date: dt.datetime
    end_date: dt.datetime
    timeframe: TimeFrame
