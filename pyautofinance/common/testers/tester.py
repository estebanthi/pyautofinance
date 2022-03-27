from abc import ABC, abstractmethod

from pyautofinance.common.results.test_result import TestResult


class Tester(ABC):

    @abstractmethod
    def test(self, strat_result) -> TestResult:
        pass
