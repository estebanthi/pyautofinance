from pyautofinance.common.testers.tester import Tester
from pyautofinance.common.simulators import MonteCarloSimulator
from pyautofinance.common.results.test_results_collection import TestResultsCollection
from pyautofinance.common.results.test_result import TestResult


class MonteCarloTester(Tester):

    def __init__(self, number_of_simulations, starting_equity, ending_equity):
        self.simulator = MonteCarloSimulator(number_of_simulations, starting_equity, ending_equity)

    def test(self, engine):
        simulation_result = self.simulator.simulate(engine)
        test_results = [TestResult(*list(metrics_collection)) for metrics_collection in simulation_result]
        return TestResultsCollection(*test_results)
