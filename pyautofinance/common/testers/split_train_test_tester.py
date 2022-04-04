from pyautofinance.common.testers.tester import Tester
from pyautofinance.common.metrics.engine_metrics import TotalGrossProfit
from pyautofinance.common.results.test_results_collection import TestResultsCollection
from pyautofinance.common.simulators.split_train_test_simulator import SplitTrainTestSimulator
from pyautofinance.common.results.test_result import TestResult


class SplitTrainTestTester(Tester):

    def __init__(self, metric_to_consider=TotalGrossProfit, test_percent=20):
        self.metric_to_consider = metric_to_consider
        self.test_percent = test_percent

    def test(self, engine):
        split_train_test_simulator = SplitTrainTestSimulator(self.metric_to_consider, self.test_percent)
        train_result, test_result = split_train_test_simulator.simulate(engine)

        train_test_result = TestResult(*train_result[0].metrics)
        test_test_result = TestResult(*test_result[0].metrics)

        return TestResultsCollection(train_test_result, test_test_result)
