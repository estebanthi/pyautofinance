from pyautofinance.common.options import DateFormat
from pyautofinance.common.config import Config


class FeedTitle:

    def __init__(self, feed_options):
        self._filename = ""
        self._set_filename_from_feed_options(feed_options)

    def get_filename(self):
        return self._filename

    def get_pathname(self):
        config = Config()
        datasets_path = config.get_datasets_pathname()
        return datasets_path + "/" + self._filename

    def _set_filename_from_feed_options(self, feed_options):
        market_options = feed_options.market_options
        time_options = feed_options.time_options
        filename_elements = []

        self._append_market_options_to_filename_elements(filename_elements, market_options)
        self._append_time_options_to_filename_elements(filename_elements, time_options)

        filename = self._get_filename_from_filename_elements(filename_elements)
        self._filename = filename

    @staticmethod
    def _append_market_options_to_filename_elements(filename_elements, market_options):
        filename_elements.append(market_options.market.value)
        filename_elements.append(market_options.symbol)

    def _append_time_options_to_filename_elements(self, filename_elements, time_options):
        start_date_str = self._format_date_for_feed_filename(time_options.start_date)
        end_date_str = self._format_date_for_feed_filename(time_options.end_date)

        filename_elements.append(start_date_str)
        filename_elements.append(end_date_str)

        filename_elements.append(time_options.timeframe.value)

    @staticmethod
    def _format_date_for_feed_filename(date):
        return date.strftime(DateFormat.FEED_FILENAME.value)

    @staticmethod
    def _get_filename_from_filename_elements(filename_elements):
        return "_".join(filename_elements) + ".csv"

