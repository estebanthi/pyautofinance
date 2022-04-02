import datetime as dt

from pyautofinance.common.testers.tester import Tester
from pyautofinance.common.metrics.engine_metrics import TotalGrossProfit


class SplitTrainTestTester(Tester):

    def test(self, engine_options, metric_to_consider=TotalGrossProfit, testing_percent=20):
        train_start_date, train_end_date, test_start_date, test_end_date = self._get_dates(engine_options, testing_percent)

        train_engine_options = self._get_train_engine_options(engine_options, train_start_date, train_end_date)

        train_engine = Engine(train_engine_options)
        train_result = train_engine.run()

        symbol = engine_options.feed_options.market_options.symbol
        best_params = train_result.get_best_params(metric_to_consider)[symbol]
        test_engine_options = self._get_test_engine_options(engine_options, test_start_date, test_end_date, symbol,
                                                            best_params)
        test_engine = Engine(test_engine_options)
        test_result = test_engine.run()
        return test_result

    def _get_dates(self, engine_options, testing_percent):
        time_options = engine_options.feed_options.time_options

        total_seconds = self._get_total_seconds_from_start_to_end(time_options.start_date, time_options.end_date)
        train_seconds = (int)(total_seconds * (100 - testing_percent) / 100)

        train_start_date = time_options.start_date
        train_end_date = train_start_date + dt.timedelta(seconds=train_seconds)

        test_start_date = train_end_date
        test_end_date = time_options.end_date

        return train_start_date, train_end_date, test_start_date, test_end_date

    @staticmethod
    def _get_total_seconds_from_start_to_end(start, end):
        return (end - start).total_seconds()

    @staticmethod
    def _get_train_engine_options(engine_options, start_date, end_date):
        updated_options = engine_options
        updated_options.feed_options.time_options.start_date = start_date
        updated_options.feed_options.time_options.end_date = end_date
        return updated_options

    @staticmethod
    def _get_test_engine_options(engine_options, start_date, end_date, symbol, strat_params):
        updated_options = engine_options
        updated_options.feed_options.time_options.start_date = start_date
        updated_options.feed_options.time_options.end_date = end_date
        updated_options.feed_options.market_options.symbol = symbol

        factory = StrategiesFactory()
        initial_strat = engine_options.strategies[0]
        updated_strat = factory.make_strategy(initial_strat.strategy, initial_strat.timeframes, **strat_params)
        updated_options.strategies[0] = updated_strat
        return updated_options