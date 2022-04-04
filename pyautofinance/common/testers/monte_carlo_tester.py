from pyautofinance.common.testers.tester import Tester
from pyautofinance.common.simulators import MonteCarloSimulator
from pyautofinance.common.results.test_result import TestResult
from pyautofinance.common.results.test_results_collection import TestResultsCollection


class MonteCarloTester(Tester):

    def __init__(self, number_of_simulations, starting_equity, ending_equity):
        self.number_of_simulations = number_of_simulations
        self.starting_equity = starting_equity
        self.ending_equity = ending_equity

    def test(self, engine):
        monte_carlo_simulator = MonteCarloSimulator(self.number_of_simulations, self.starting_equity,
                                                    self.ending_equity)

        engine_result = engine.run()

        tests_results = []
        for strat_result in engine_result:
            trades = strat_result.trades
            simulation_result = monte_carlo_simulator.simulate(trades)
            metrics = [metric for metric in simulation_result.values()]
            test_result = TestResult(*metrics)
            tests_results.append(test_result)
        return TestResultsCollection(*tests_results)
