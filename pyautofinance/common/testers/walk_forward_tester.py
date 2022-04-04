from pyautofinance.common.testers.tester import Tester
from pyautofinance.common.metrics.engine_metrics import TotalGrossProfit
from pyautofinance.common.results.test_results_collection import TestResultsCollection
from pyautofinance.common.simulators.walk_forward_simulator import WalkForwardSimulator
from pyautofinance.common.results.test_result import TestResult


class WalkForwardTester(Tester):

    def __init__(self, periods=1, metric_to_consider=TotalGrossProfit, test_percent=20, anchored=False):
        self.periods = periods
        self.metric_to_consider = metric_to_consider
        self.test_percent = test_percent
        self.anchored = anchored

    def test(self, engine):
        walk_forward_simulator = WalkForwardSimulator(self.periods, self.metric_to_consider, self.test_percent,
                                                      self.anchored)

        result = walk_forward_simulator.simulate(engine)
        train_results = [res[0] for res in result]
        test_results = [res[1] for res in result]

        train_metrics = [engine_result[0].metrics for engine_result in train_results]
        train_test_results = [TestResult(*metrics.values()) for metrics in train_metrics]
        test_metrics = [engine_result[0].metrics for engine_result in test_results]
        test_test_results = [TestResult(*metrics.values()) for metrics in test_metrics]

        return TestResultsCollection(*train_test_results, *test_test_results)
