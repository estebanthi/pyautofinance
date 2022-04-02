from abc import ABC, abstractmethod

from pyautofinance.common.results.test_result import TestResult
from pyautofinance.common.results.engine_result import EngineResult


class Tester(ABC):

    @abstractmethod
    def test(self, engine_result: EngineResult) -> TestResult:
        pass

    @abstractmethod
    def validate(self, test_result):
        pass
