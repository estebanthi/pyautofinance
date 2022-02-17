from enums.DateFormat import DateFormat


def format_date_for_feed_filename(date):
    return date.strftime(DateFormat.FEED_FILENAME.value)
