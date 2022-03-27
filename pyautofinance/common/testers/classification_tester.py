from sklearn.metrics import classification_report

from pyautofinance.common.testers.tester import Tester


class ClassificationTester(Tester):

    def test(self, engine_options):
        y_true = self._predicter.get_real_outputs(back_datafeed)
        y_pred = self._predicter.predict(back_datafeed)
        return classification_report(y_true, y_pred)
