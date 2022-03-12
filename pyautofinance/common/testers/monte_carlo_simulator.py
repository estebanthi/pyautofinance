import random


class MonteCarloSimulator:

    def __init__(self, trades_collection):
        self._trades_collection = trades_collection
        random.shuffle(self._trades_collection)
