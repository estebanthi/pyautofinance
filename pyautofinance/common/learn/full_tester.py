from sklearn.metrics import classification_report

from pyautofinance.common.learn.tester import Tester


class FullTester(Tester):

    def test(self, back_datafeed):
        real = self._predicter.get_real_outputs(back_datafeed)
        predictions = self._predicter.predict(back_datafeed)
        print(classification_report(real, predictions))