from pyautofinance.common.testers.tester import Tester
from pyautofinance.common.simulators.monkey_simulator import MonkeySimulator
from pyautofinance.common.metrics.monkey_metrics import ProfitDifference
from pyautofinance.common.results.test_result import TestResult
from pyautofinance.common.results.test_results_collection import TestResultsCollection


class MonkeyTester(Tester):

    def __init__(self, monkey_strat, iterations=8000):
        self.iterations = iterations
        self.monkey_strat = monkey_strat

    def test(self, engine):
        engine_result = engine.run()

        simulator = MonkeySimulator(self.monkey_strat, self.iterations)
        engine_results_collection = simulator.simulate(engine)
        average_monkey_profit = engine_results_collection.get_average_metric('TotalGrossProfit')[0]

        return self._build_test_results_collection(engine_result, average_monkey_profit)

    @staticmethod
    def _build_test_results_collection(engine_result, average_monkey_profit):
        test_results = []
        for strat_result in engine_result:
            total_gross_profit = strat_result['TotalGrossProfit'].value
            profit_difference = ProfitDifference(total_gross_profit, average_monkey_profit)
            test_results.append(TestResult(profit_difference))

        return TestResultsCollection(*test_results)
