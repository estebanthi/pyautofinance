from abc import ABC, abstractmethod

from sklearn.metrics import classification_report

from pyautofinance.common.learn.predicter import Predicter


class Tester(ABC):

    def __init__(self, predicter: Predicter):
        self._predicter = predicter

    @abstractmethod
    def test(self, back_datafeed):
        pass
