from abc import ABC, abstractmethod

from pyautofinance.common.results.test_result import TestResult
from pyautofinance.common.results.engine_result import EngineResult
from pyautofinance.common.metrics.metric import Metric


class Tester(ABC):

    @abstractmethod
    def test(self, engine_result: EngineResult) -> TestResult:
        pass

    @staticmethod
    def validate(test_result, metric, validation_function):
        metric_name = metric if isinstance(metric, str) else metric.name
        metric_value = test_result[metric_name].value

        valid = validation_function(metric_value)
        test_result.valid = valid

        return valid