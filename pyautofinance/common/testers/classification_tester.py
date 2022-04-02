from pyautofinance.common.testers.tester import Tester
from pyautofinance.common.metrics.learn_metrics import F1Score, Accuracy, Recall, Precision
from pyautofinance.common.results.test_result import TestResult


class ClassificationTester(Tester):

    def __init__(self, predicter):
        self._predicter = predicter

    def test(self, engine_result):
        back_datafeed = engine_result.datafeed

        y_true = self._predicter.get_real_outputs(back_datafeed)
        y_pred = self._predicter.predict(back_datafeed)

        f1_score = F1Score(y_true, y_pred)
        accuracy = Accuracy(y_true, y_pred)
        precision = Precision(y_true, y_pred)
        recall = Recall(y_true, y_pred)

        return TestResult(f1_score, accuracy, precision, recall)

