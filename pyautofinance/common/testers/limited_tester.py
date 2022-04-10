from pyautofinance.common.testers.tester import Tester
from pyautofinance.common.results.test_results_collection import TestResultsCollection


class MonkeyTester(Tester):

    def __init__(self, limited_strat):
        self.limited_strat = limited_strat

    def test(self, engine):
        engine.components_assembly[1] = self.limited_strat
        engine_result = engine.run()

        test_results = [strat_result['Winrate'] for strat_result in engine_result]
        return TestResultsCollection(*test_results)
