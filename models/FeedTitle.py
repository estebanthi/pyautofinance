from utils.dates import format_date_for_feed_filename
from models.Config.Config import Config


class FeedTitle:

    def __init__(self, feed_options):
        self.filename = ""
        self.set_filename_from_feed_options(feed_options)

    def set_filename_from_feed_options(self, feed_options):
        filename_characteristics = []

        filename_characteristics.append(feed_options.market_options.market.value)
        filename_characteristics.append(feed_options.market_options.symbol)

        start_date_str = format_date_for_feed_filename(feed_options.time_options.start_date)
        end_date_str = format_date_for_feed_filename(feed_options.time_options.end_date)
        filename_characteristics.append(start_date_str)
        filename_characteristics.append(end_date_str)

        filename_characteristics.append(feed_options.time_options.timeframe.value)

        self.filename = "_".join(filename_characteristics) + ".csv"

    def get_filename(self):
        return self.filename

    def get_pathname(self):
        config = Config()
        datasets_path = config.get_datasets_pathname()

        return datasets_path + "/" + self.filename
