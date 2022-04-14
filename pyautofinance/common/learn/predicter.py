from abc import ABC, abstractmethod

import pickle

from pyautofinance.common.config.config import Config


class Predicter(ABC):

    def __init__(self, filename=None, from_=None, **kwargs):
        config = Config()
        pathname = from_ if from_ else config['predicters_pathname']

        if filename:
            with open(f"{pathname}/{filename}.prd", 'rb') as file:
                predicter = pickle.load(file)
            self._copy(predicter)

        else:
            self._init_predicter(**kwargs)

    @abstractmethod
    def _copy(self, other):
        pass

    @abstractmethod
    def _init_predicter(self):
        pass

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

    def save(self, filename, to=None):
        config = Config()
        pathname = to if to else config['predicters_pathname']

        with open(f"{pathname}/{filename}.prd", 'wb') as file:
            pickle.dump(self, file)
