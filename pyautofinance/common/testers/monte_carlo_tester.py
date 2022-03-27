from pyautofinance.common.testers.tester import Tester
from pyautofinance.common.testers.monte_carlo_simulator import MonteCarloSimulator
from pyautofinance.common.results.test_result import TestResult


class MonteCarloTester(Tester):

    def __init__(self, number_of_simulations, starting_equity, ending_equity):
        self.number_of_simulations = number_of_simulations
        self.starting_equity = starting_equity
        self.ending_equity = ending_equity

    def test(self, strat_result):
        monte_carlo_simulator = MonteCarloSimulator(self.number_of_simulations, self.starting_equity,
                                                    self.ending_equity)
        trades = strat_result.trades
        simulation_result = monte_carlo_simulator.simulate(trades)

        metrics = [metric for metric in simulation_result.values()]
        test_result = TestResult(*metrics)
        return test_result
