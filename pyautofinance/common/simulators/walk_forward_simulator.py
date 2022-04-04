import datetime as dt

from pyautofinance.common.simulators.split_train_test_simulator import SplitTrainTestSimulator
from pyautofinance.common.metrics.engine_metrics import TotalGrossProfit


class WalkForwardSimulator:

    def __init__(self, periods, metric_to_consider=TotalGrossProfit, testing_percent=20, anchored=False):
        self.periods = periods
        self.metric_to_consider = metric_to_consider
        self.testing_percent = testing_percent
        self.anchored = anchored

    def simulate(self, engine):
        split_train_test_simulator = SplitTrainTestSimulator(self.metric_to_consider, self.testing_percent)
        start_dates, end_dates = self._get_dates(engine)
        results = []
        for start_date, end_date in zip(start_dates, end_dates):
            engine.components_assembly[2].start_date = start_date
            engine.components_assembly[2].end_date = end_date

            train_result, test_result = split_train_test_simulator.simulate(engine)
            results.append((train_result, test_result))

        return results

    def _get_dates(self, engine):
        back_datafeed = engine.components_assembly[2]
        ohlcv = back_datafeed.ohlcv

        start_date = ohlcv.start_date
        end_date = ohlcv.end_date

        total_seconds = self._get_total_seconds_from_start_to_end(start_date, end_date)
        seconds_per_period = total_seconds / self.periods

        start_dates = [start_date + dt.timedelta(seconds=seconds_per_period) * i for i in range(self.periods)] \
            if not self.anchored else [start_date for i in range(self.periods)]

        end_dates = [start_date + dt.timedelta(seconds=seconds_per_period) * i for i in range(1, self.periods + 1)]

        return start_dates, end_dates

    @staticmethod
    def _get_total_seconds_from_start_to_end(start, end):
        return (end - start).total_seconds()
