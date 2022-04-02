import datetime as dt

from pyautofinance.common.metrics.engine_metrics import TotalGrossProfit
from pyautofinance.common.engine.engine import Engine


class SplitTrainTestSimulator:

    def __init__(self, metric_to_consider=TotalGrossProfit, testing_percent=20):
        self.metric_to_consider = metric_to_consider
        self.testing_percent = testing_percent

    def test(self, engine):
        train_start_date, train_end_date, test_start_date, test_end_date = self._get_dates(engine, self.testing_percent)
        print(train_start_date, train_end_date, test_start_date, test_end_date)

        train_engine = self._get_train_engine(engine, train_start_date, train_end_date)
        train_result = train_engine.run()

        best_params = train_result.get_best_params(self.metric_to_consider.name)
        best_params = dict(best_params)
        best_params.pop('timeframes')
        test_engine = self._get_test_engine(engine, test_start_date, test_end_date, best_params)
        test_result = test_engine.run()
        return test_result

    def _get_dates(self, engine, testing_percent):
        back_datafeed = engine.components_assembly[2]
        ohlcv = back_datafeed.ohlcv

        start_date = ohlcv.start_date
        end_date = ohlcv.end_date

        total_seconds = self._get_total_seconds_from_start_to_end(start_date, end_date)
        train_seconds = (int)(total_seconds * (100 - testing_percent) / 100)

        train_start_date = start_date
        train_end_date = train_start_date + dt.timedelta(seconds=train_seconds)

        test_start_date = train_end_date
        test_end_date = end_date

        return train_start_date, train_end_date, test_start_date, test_end_date

    @staticmethod
    def _get_total_seconds_from_start_to_end(start, end):
        return (end - start).total_seconds()

    @staticmethod
    def _get_train_engine(engine, start_date, end_date):
        engine.components_assembly[2].start_date = start_date
        engine.components_assembly[2].end_date = end_date
        return engine

    @staticmethod
    def _get_test_engine(engine, start_date, end_date, strat_params):
        engine.components_assembly[2].start_date = start_date
        engine.components_assembly[2].end_date = end_date

        engine.components_assembly[1].set_parameters(strat_params)
        return engine