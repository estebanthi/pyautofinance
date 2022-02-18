from dataclasses import dataclass
import datetime as dt
from enums import TimeFrame
from exceptions.feeds.EndDateBeforeStartDate import EndDateBeforeStartDate


@dataclass
class TimeOptions:
    start_date: dt.datetime
    end_date: dt.datetime
    timeframe: TimeFrame

    def __post_init__(self):
        if self.end_date < self.start_date:
            raise EndDateBeforeStartDate
