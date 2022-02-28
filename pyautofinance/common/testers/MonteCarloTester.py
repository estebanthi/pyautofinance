from itertools import permutations

from pyautofinance.common.testers.Tester import Tester


class MonteCarloTester(Tester):

    def test(self, engine_options):
        pass

    def multitest(self, engine_options, symbols):
        pass

    @staticmethod
    def get_all_trades_combinations(trades):
        return [list(p) for p in permutations(trades)]

