import unittest
import datetime as dt

from pyautofinance.common.exceptions.feeds import EndDateBeforeStartDate

from pyautofinance.common.options import TimeOptions, TimeFrame


class TestTimeOptions(unittest.TestCase):

    start_date = dt.datetime(2020, 1, 1, 0, 0, 0)
    end_date_ok = dt.datetime(2021, 1, 1, 0, 0, 0)
    end_date_nok = dt.datetime(2019, 1, 1, 0, 0, 0)
    timeframe = TimeFrame.d1

    def test_dates_ok(self):
        time_options = TimeOptions(self.start_date, end_date=self.end_date_ok, timeframe=self.timeframe)

    def test_dates_nok(self):
        with self.assertRaises(EndDateBeforeStartDate):
            time_options = TimeOptions(self.start_date, end_date=self.end_date_nok, timeframe=self.timeframe)


if __name__ == '__main__':
    unittest.main()
