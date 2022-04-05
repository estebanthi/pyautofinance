from pyautofinance.common.testers.tester import Tester
from pyautofinance.common.simulators.monkey_simulator import MonkeySimulator


class MonkeyTester(Tester):

    def __init__(self, iterations=8000, monkey_full=None, monkey_entry=None, monkey_exit=None):
        self.iterations = iterations
        self.monkey_full = monkey_full
        self.monkey_entry = monkey_entry
        self.monkey_exit = monkey_exit

    def test(self, engine):
        simulator = MonkeySimulator(self.iterations, self.monkey_full, self.monkey_entry, self.monkey_exit)
        results = simulator.simulate(engine)
        