from abc import ABC, abstractmethod

from pyautofinance.common.results.test_result import TestResult
from pyautofinance.common.results.engine_result import EngineResult
from pyautofinance.common.results.strat_result import StratResult
from pyautofinance.common.results.test_results_collection import TestResultsCollection


class Tester(ABC):

    def test(self, engine_result: EngineResult) -> TestResult:
        test_results = []
        for strat in engine_result:
            test_results.append(self._test_for_strat(strat))
        return TestResultsCollection(*test_results)

    @abstractmethod
    def _test_for_strat(self, strat_result: StratResult) -> TestResult:
        pass
