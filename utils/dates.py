import datetime as dt
from enums.DateFormat import DateFormat


def format_date_for_feed_filename(date):
    return date.strftime(DateFormat.FEED_FILENAME.value)

def epoch_to_datetime(epoch):
    epoch /= 1000
    return dt.datetime.fromtimestamp(epoch)
