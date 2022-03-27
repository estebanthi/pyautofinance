from abc import ABC, abstractmethod


class Predicter(ABC):

    @abstractmethod
    def predict(self, x) -> int:
        pass

    @abstractmethod
    def fit(self, back_datafeed):
        pass

    @abstractmethod
    def get_real_outputs(self, back_datafeed):
        # For a datafeed, returns the best decisions possible
        pass
