from abc import ABC, abstractmethod

from pyautofinance.common.results.test_result import TestResult
from pyautofinance.common.results.test_results_collection import TestResultsCollection
from pyautofinance.common.engine import Engine


class Tester(ABC):

    @abstractmethod
    def test(self, engine: Engine):
        pass
